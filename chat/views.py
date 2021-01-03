import json
from django.core import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

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


class ConversationView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = forms.ConversationForm
    template_name = 'chat/conversation_view.html'

    def dispatch(self, request, *args, **kwargs):
        self.conversation = Conversation.objects.get(pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        conversation_messages = self.conversation.message_set.all()
        conversation_messages_serialized = \
            serializers.serialize('json', conversation_messages)
        conversation_messages_json = \
            json.loads(conversation_messages_serialized)

        conversation_users = UserModel.objects.filter(pk__in=
            [user.pk for user in 
                [message.sender for message in conversation_messages]])
        conversation_users_serialized = \
            serializers.serialize('json', conversation_users)
        conversation_users_json = \
            json.loads(conversation_users_serialized)


        context.update({
            'conversation_messages': conversation_messages_json,
            'conversation_users': conversation_users_json})
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.conversation = self.conversation
        self.object.sender = self.request.user
        return super().form_valid(form)


class MessageListView(ListView):
    model = Message
    template_name = 'chat/chat_list.html'
