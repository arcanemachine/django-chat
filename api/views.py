from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .permissions import HasMessagePermissionsOrReadOnly
from chat.models import Conversation, Message

UserModel = get_user_model()

#class MessageCreate(generics.APIView):
#    permission_classes = [HasMessagePermissionsOrReadOnly]
#    serializer_class = serializers.MessageSerializer
#
#    def get_queryset(self):
#        return Conversation.objects.filter(pk=self.kwargs['conversation_pk'])


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [HasMessagePermissionsOrReadOnly]
    serializer_class = serializers.MessageSerializer
    lookup_url_kwarg = 'message_pk'

    def get_queryset(self):
        return Message.objects.filter(pk=self.kwargs['message_pk'])
