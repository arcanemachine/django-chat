import json
from django.contrib.auth import get_user_model
from django.utils import timezone
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

    def to_representation(self, instance):
        def iso_time(dt_obj):
            date_handler = lambda obj: (
                obj.isoformat()
                if isinstance(obj, (timezone.datetime, timezone.datetime.date))
                else None)
            return json.loads(json.dumps(dt_obj, default=date_handler))

        result = {
            'pk': instance.pk,
            'conversation': instance.conversation.pk,
            'sender': instance.sender.pk if instance.sender else None,
            'sender_username': instance.sender_username,
            'content': instance.content,
            'created_at': iso_time(instance.created_at),
            'modified_at': iso_time(instance.modified_at),
            'all_messages_shown': self.fields['all_messages_shown'].default}
        return result
        #if 'all_messages_shown' in self.fields:
        #    result.update({
        #        'all_messages_shown': self.fields['all_messages_shown']})



    def __init__(self, *args, **kwargs):
        # if the requested amount of messages is >= the conversation's
        # message count, then all_messages_shown = True
        if 'context' in kwargs:
            context = kwargs['context']
            if 'all_messages_shown' in context:
                if context['all_messages_shown'] is True:
                    self.fields['all_messages_shown'].default = True
                #elif context['all_messages_shown'] == 'disabled':
                #    del self.fields['all_messages_shown']

        super().__init__(*args, **kwargs)


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['pk', 'conversation', 'sender', 'sender_username', 'content',
                  'created_at']

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message
