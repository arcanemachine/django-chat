from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
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


class UserList(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return UserModel.objects.all()


class ConversationUserList(generics.ListAPIView):
    permission_classes = [HasConversationPermissions]
    serializer_class = serializers.UserSerializer
    lookup_url_kwargs = 'conversation_pk'

    def get_queryset(self):
        return Conversation.objects.get(
            pk=self.kwargs['conversation_pk']).participants.all()


class UserDetail(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer
    lookup_url_kwargs = 'user_pk'

    def get_queryset(self):
        return UserModel.objects.filter(pk=self.kwargs['user_pk'])


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


class MessageListCreateLast(generics.ListCreateAPIView):
    permission_classes = [HasConversationPermissions]
    serializer_class = serializers.MessageSerializer
    lookup_url_kwarg = 'conversation_pk'

    def get_queryset(self):
        return Conversation.objects.get(
            pk=self.kwargs['conversation_pk']).message_set.filter(pk__in=[1])


class MessageListCount(generics.ListAPIView):
    """Get the newest n messages from a conversation."""
    permission_classes = [HasMessagePermissions]
    serializer_class = serializers.MessageSerializer
    lookup_url_kwarg = 'conversation_pk'

    def dispatch(self, request, *args, **kwargs):
        self.conversation = \
            Conversation.objects.get(pk=self.kwargs['conversation_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        all_messages_shown = True if self.kwargs['message_count'] >= \
            self.conversation.message_set.count() else False
        context.update({
            'request_method': self.request.method,
            'all_messages_shown': all_messages_shown})
        return context

    def get_queryset(self):
        return self.conversation.message_set \
            .order_by('-pk')[:self.kwargs['message_count']]


class MessageListRange(generics.ListAPIView):
    """Get the x-newest to y-newest messages from a conversation."""
    permission_classes = [HasMessagePermissions]
    serializer_class = serializers.MessageSerializer
    lookup_url_kwarg = 'conversation_pk'

    def get_queryset(self):
        range_from = self.kwargs['range_from']
        range_to = self.kwargs['range_to']
        messages = Conversation.objects.get(pk=self.kwargs['conversation_pk'])\
            .message_set.order_by('-pk')\
            .filter(pk__gte=range_from)
        if range_to != 0:
            messages = messages.filter(pk__lte=range_to)
        return messages


class MessageCreate(generics.CreateAPIView):
    """Add a new message to an existing conversation."""
    permission_classes = [HasConversationPermissions]
    serializer_class = serializers.MessageCreateSerializer
    lookup_url_kwarg = 'conversation_pk'

    def get_queryset(self):
        return Conversation.objects.filter(pk=self.kwargs['conversation_pk'])

    def post(self, request, *args, **kwargs):
        request.data.update({
            'conversation': self.get_queryset().first().pk,
            'sender': request.user.pk,
            'sender_username': request.user.username})
        return super().post(request, *args, **kwargs)


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [HasMessagePermissions]
    serializer_class = serializers.MessageSerializer
    lookup_url_kwarg = 'message_pk'

    def get_queryset(self):
        return Message.objects.filter(pk=self.kwargs['message_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['all_messages_shown'] = 'disabled'
        return context
