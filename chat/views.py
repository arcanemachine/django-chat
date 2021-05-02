import json
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.staticfiles import finders
from django.http import JsonResponse, HttpResponseForbidden
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


class ConversationCreateView(CreateView):
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

        # if user has unread messages,
        # add the pk of the last-read message to the context
        unread_messages = self.request.user.profile.unread_messages
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


class MessageListView(ListView):
    model = Message
    template_name = 'chat/chat_list.html'
