from rest_framework import serializers

from chat.models import Message

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['pk', 'conversation', 'sender', 'sender_username', \
            'content', 'created_at', 'modified_at']
        read_only_fields = ['conversation', 'sender', 'sender_username', \
            'created_at', 'modified_at']
