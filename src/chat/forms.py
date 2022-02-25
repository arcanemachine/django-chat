from django import forms
from django.contrib.auth import get_user_model

from .models import Conversation, Message

UserModel = get_user_model()


class ConversationCreateForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['subject', 'participants']
        widgets = {
            'subject': forms.TextInput(attrs={'size': 30}),
            'participants': forms.CheckboxSelectMultiple(),
        }


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(),
        }
