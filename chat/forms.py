from django import forms
from django.contrib.auth import get_user_model

from .models import Message

UserModel = get_user_model()


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(),
        }
