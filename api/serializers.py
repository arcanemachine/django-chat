from django.contrib.auth import get_user_model
from rest_framework import serializers

from chat.models import Message

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['pk', 'username']
        read_only_fields = ('all',)


class MessageSerializer(serializers.ModelSerializer):

    all_messages_shown = serializers.BooleanField(default=False)

    class Meta:
        model = Message
        fields = ['pk', 'conversation', 'sender', 'sender_username',
                  'content', 'created_at', 'modified_at', 'all_messages_shown']
        read_only_fields = ['conversation', 'sender', 'sender_username',
                            'created_at', 'modified_at', 'all_messages_shown']

    def __init__(self, *args, **kwargs):
        # if the requested amount of messages is >= the conversation's
        # message count, then all_messages_shown = True
        if 'context' in kwargs:
            context = kwargs['context']
            if 'all_messages_shown' in context \
                    and context['all_messages_shown'] is True:
                self.fields['all_messages_shown'].default = True
        super().__init__(*args, **kwargs)


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['pk', 'conversation', 'sender', 'sender_username', 'content']

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message
