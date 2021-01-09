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
        if 'message_set_count' in kwargs['context'] \
                and 'message_count' in kwargs['context'] \
                and kwargs['context']['message_count'] >= \
                    kwargs['context']['message_set_count']:
            self.fields['all_messages_shown'].default = True
        super().__init__(*args, **kwargs)


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['pk', 'conversation', 'sender', 'sender_username', 'content']

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message
