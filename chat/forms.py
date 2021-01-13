from django import forms
from django.contrib.auth import get_user_model

from .models import Conversation, Message

UserModel = get_user_model()


class ConversationCreateForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['subject', 'participants']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        breakpoint()
        self.fields['subject'].widget.attrs['size'] = 20


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(),
        }
