from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .permissions import HasConversationPermissions, HasMessagePermissions
from chat.models import Conversation, Message

UserModel = get_user_model()


# class MessageCreate(generics.APIView):
#     permission_classes = [HasMessagePermissions]
#     serializer_class = serializers.MessageSerializer
#
#     def get_queryset(self):
#         return Conversation.objects.filter(pk=self.kwargs['conversation_pk'])


@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({
            'message': "You sent a POST request!",
            'data': request.data})
    return Response({'message': "Hello world!"})


class MessageList(generics.ListAPIView):
    permission_classes = [HasConversationPermissions]
    serializer_class = serializers.MessageSerializer
    lookup_url_kwarg = 'conversation_pk'

    def get_queryset(self):
        return Conversation.objects.get(
            pk=self.kwargs['conversation_pk']).message_set.order_by('-pk')


class MessageListCreate(generics.ListCreateAPIView):
    permission_classes = [HasConversationPermissions]
    serializer_class = serializers.MessageSerializer
    lookup_url_kwarg = 'conversation_pk'

    def get_queryset(self):
        return Conversation.objects.get(
            pk=self.kwargs['conversation_pk']).message_set.order_by('-pk')


class MessageListCount(generics.ListAPIView):
    """Get the newest n messages from a conversation."""
    permission_classes = [HasMessagePermissions]
    serializer_class = serializers.MessageSerializer
    lookup_url_kwarg = 'conversation_pk'

    def get_queryset(self):
        return Conversation.objects.get(pk=self.kwargs['conversation_pk'])\
            .message_set.order_by('-pk')[:self.kwargs['message_count']]


class MessageListRange(generics.ListAPIView):
    """Get the x-newest to y-newest messages from a conversation."""
    permission_classes = [HasMessagePermissions]
    serializer_class = serializers.MessageSerializer
    lookup_url_kwarg = 'conversation_pk'

    def get_queryset(self):
        range_from = self.kwargs['range_from']
        range_to = self.kwargs['range_to']
        messages = Conversation.objects.get(pk=self.kwargs['conversation_pk'])\
            .message_set.order_by('-pk')
        if range_to == 0:
            range_to = messages.count()
        return messages[range_from:range_to]


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [HasMessagePermissions]
    serializer_class = serializers.MessageSerializer
    lookup_url_kwarg = 'message_pk'

    def get_queryset(self):
        return Message.objects.filter(pk=self.kwargs['message_pk'])
