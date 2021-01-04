from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .permissions import HasMessagePermissionsOrReadOnly
from chat.models import Message

UserModel = get_user_model()

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [HasMessagePermissionsOrReadOnly]
    serializer_class = serializers.MessageSerializer
    lookup_url_kwarg = 'message_pk'

    def get_queryset(self):
        return Message.objects.filter(pk=self.kwargs['message_pk'])
