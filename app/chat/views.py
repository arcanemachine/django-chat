import json
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import \
    JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView

from . import forms
from .models import Conversation, Message
from api.serializers import MessageSerializer

UserModel = get_user_model()


def chat_root(request):
    return render(request, 'chat/chat_root.html')


class ConversationListView(ListView):
    model = Conversation
    template_name = 'chat/chat_list.html'


class ConversationCreateView(LoginRequiredMixin, CreateView):
    model = Conversation
    form_class = forms.ConversationCreateForm
    template_name = 'chat/conversation_create.html'
    success_message = "New conversation successfully created."

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user not in self.object.participants.all():
            self.object.participants.add(self.request.user)
        return super().form_valid(form)


class ConversationView(UserPassesTestMixin, CreateView):
    model = Message
    form_class = forms.ConversationForm
    template_name = 'chat/conversation_view.html'

    def dispatch(self, request, *args, **kwargs):
        self.conversation = \
            get_object_or_404(Conversation, pk=self.kwargs['conversation_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # serialize the conversation messages
        conversation_messages = \
            self.conversation.message_set.order_by('-pk')[:20]
        conversation_messages_serialized = \
            MessageSerializer(conversation_messages, many=True).data
        conversation_messages_json = \
            json.loads(json.dumps(conversation_messages_serialized))

        if self.request.user.is_authenticated:
            # if user has unread messages,
            # add the pk of the last-read message to the context
            unread_messages = self.request.user.profile.unread_messages
        else:
            unread_messages = None
        if unread_messages:
            if str(self.conversation.pk) in unread_messages:
                context['last_read_message_pk'] = \
                    unread_messages.pop(str(self.conversation.pk))
                messages.info(
                    self.request,
                    "New messages are shown with a glowing red border.")
                self.request.user.save()

        all_conversation_messages_count = self.conversation.message_set.count()

        context.update({
            'conversation': self.conversation,
            'conversation_messages': conversation_messages_json,
            'all_messages_loaded_from_db':
                True if all_conversation_messages_count ==
                conversation_messages.count() else False})
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.conversation = self.conversation
        self.object.sender = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return True  # allow users to post in any chat
        # return self.request.user in self.conversation.participants.all()


class ConversationUpdateParticipantsView(LoginRequiredMixin, UpdateView):
    model = Conversation
    fields = ('participants',)
    template_name = 'chat/conversation_update_participants.html'
    success_message = "Participant list updated"
    pk_url_kwarg = 'conversation_pk'

    def form_valid(self, form):
        # require user to be in conversation
        participants_qs = form.cleaned_data['participants']
        if self.request.user not in participants_qs:
            participants_list = \
                [user.pk for user in participants_qs] + [self.request.user.pk]
            participants_qs = \
                UserModel.objects.filter(pk__in=participants_list)
            form.cleaned_data['participants'] = participants_qs
            messages.info(self.request,
                          "You cannot remove yourself from a conversation. "
                          "We have added you back to the conversation.")
        messages.info(self.request, "Conversation participants updated.")
        return super().form_valid(form)


def json_hello_world(request):
    result = {'hello': 'world'}
    return JsonResponse(result)


def json_debug(request):
    if request.user.username == 'admin':
        breakpoint()
        return JsonResponse({'username': request.user.username})
    return HttpResponseForbidden()


def json_user_is_logged_in(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'You are not logged in.'})
    elif request.user.is_authenticated:
        return JsonResponse(
            {'message': f"You are logged in as {request.user.username}"})


def json_reverse_url(request, reverse_string):
    try:
        request_get_dict = dict(request.GET)
        for item in request_get_dict.keys():
            request_get_dict[item] = request_get_dict[item][0]
        url = reverse(reverse_string, kwargs=request_get_dict)
        return JsonResponse({'url': url})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def get_conversation_messages(request, conversation_pk, message_count):
    try:
        conversation = Conversation.objects.get(pk=conversation_pk)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

    messages = conversation.message_set.order_by('-pk')[:message_count]
    messages_serialized = serializers.serialize('json', messages)
    messages_json = json.loads(messages_serialized)

    all_messages_shown = messages.count() == conversation.message_set.count()

    result = {'messages': messages_json,
              'allMessagesShown': all_messages_shown}

    return JsonResponse(result, safe=False)


def get_conversation_message(request, conversation_pk, message_pk):
    try:
        conversation = Conversation.objects.get(pk=conversation_pk)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

    message = conversation.message_set.filter(pk=message_pk)

    if not message.exists():
        return JsonResponse(
            {'error': "There is no message matching the ID entered."},
            status=404)

    message_serialized = serializers.serialize('json', message)
    message_json = json.loads(message_serialized)

    result = {'message': message_json}

    return JsonResponse(result, safe=False)


def get_conversation_users(request, conversation_pk):
    try:
        conversation = Conversation.objects.get(pk=conversation_pk)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

    users = conversation.participants.all()
    users_serialized = serializers.serialize('json', users)
    users_json = json.loads(users_serialized)

    return JsonResponse(users_json, safe=False)


def create_conversation_message(request, conversation_pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Please login first'}, status=401)

    try:
        conversation = Conversation.objects.get(pk=conversation_pk)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

    if request.method == 'POST':
        try:
            message_content = \
                json.loads(request.body.decode('utf-8'))['content']

            new_message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=message_content)

            new_message_qs = conversation.message_set.filter(pk=new_message.pk)
            message_serialized = serializers.serialize('json', new_message_qs)
            message_json = json.loads(message_serialized)

            result = {'newMessage': message_json}
            return JsonResponse(result)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        # return message pk
        return JsonResponse({'message': 'POST request received'})
    else:
        return JsonResponse(
            {'message': 'This view supports POST requests only'}, status=405)


class MessageListView(ListView):
    model = Message
    template_name = 'chat/chat_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('chat:conversation_list'))
        return super().dispatch(request, *args, **kwargs)
