import json
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView

from . import forms
from .models import Conversation, Message

UserModel = get_user_model()


def chat_root(request):
    return render(request, 'chat/chat_root.html')


class ConversationListView(ListView):
    model = Conversation
    template_name = 'chat/chat_list.html'


class ConversationCreateView(CreateView):
    model = Conversation
    fields = ('subject', 'participants')
    template_name = 'chat/conversation_create.html'
    success_message = "New conversation successfully created."

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user not in self.object.participants.all():
            self.object.participants.add(self.request.user)
        return super().form_valid(form)


class ConversationView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Message
    form_class = forms.ConversationForm
    template_name = 'chat/conversation_view.html'

    def dispatch(self, request, *args, **kwargs):
        self.conversation = \
            Conversation.objects.get(pk=self.kwargs['conversation_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        conversation_messages = \
            self.conversation.message_set.order_by('-pk')[:10]
        conversation_messages_serialized = \
            serializers.serialize('json', conversation_messages)
        conversation_messages_json = \
            json.loads(conversation_messages_serialized)

        context.update({
            'conversation': self.conversation,
            'conversation_messages': conversation_messages_json
            })
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.conversation = self.conversation
        self.object.sender = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user in self.conversation.participants.all()

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
                          "You cannot remove yourself from a conversation."
                          "You have been added back to the conversation.")
        messages.info(self.request, "Conversation participants updated.")
        return super().form_valid(form)


def test_message(request):
    result = {'hello': 'world'}
    return JsonResponse(result)


def get_conversation_messages(request, conversation_pk, number_of_messages):
    conversation = Conversation.objects.get(pk=conversation_pk)

    messages = conversation.message_set.order_by('-pk')[:number_of_messages]
    messages_serialized = serializers.serialize('json', messages)
    messages_json = json.loads(messages_serialized)

    all_messages_shown = messages.count() == conversation.message_set.count()

    result = {'messages': messages_json,
              'allMessagesShown': all_messages_shown}

    return JsonResponse(result, safe=False)


def get_conversation_users(request, conversation_pk):
    conversation = Conversation.objects.get(pk=conversation_pk)

    users = conversation.participants.all()
    users_serialized = serializers.serialize('json', users)
    users_json = json.loads(users_serialized)

    return JsonResponse(users_json, safe=False)


class MessageListView(ListView):
    model = Message
    template_name = 'chat/chat_list.html'
