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


def json_hello_world(request):
    result = {'hello': 'world'}
    return JsonResponse(result)


def json_debug(request):
    if request.user.username == 'admin':
        breakpoint()
        return JsonResponse({'username': request.user.username})
    return HttpResponseForbidden()


def json_user_is_logged_in(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'You are not logged in.'})
    elif request.user.is_authenticated:
        return JsonResponse(
            {'message': f"You are logged in as {request.user.username}"})


def json_reverse_url(request, reverse_string):
    try:
        request_get_dict = dict(request.GET)
        for item in request_get_dict.keys():
            request_get_dict[item] = request_get_dict[item][0]
        url = reverse(reverse_string, kwargs=request_get_dict)
        return JsonResponse({'url': url})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def get_conversation_messages(request, conversation_pk, message_count):
    try:
        conversation = Conversation.objects.get(pk=conversation_pk)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

    messages = conversation.message_set.order_by('-pk')[:message_count]
    messages_serialized = serializers.serialize('json', messages)
    messages_json = json.loads(messages_serialized)

    all_messages_shown = messages.count() == conversation.message_set.count()

    result = {'messages': messages_json,
              'allMessagesShown': all_messages_shown}

    return JsonResponse(result, safe=False)


def get_conversation_message(request, conversation_pk, message_pk):
    try:
        conversation = Conversation.objects.get(pk=conversation_pk)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

    message = conversation.message_set.filter(pk=message_pk)

    if not message.exists():
        return JsonResponse(
            {'error': "There is no message matching the ID entered."},
            status=404)

    message_serialized = serializers.serialize('json', message)
    message_json = json.loads(message_serialized)

    result = {'message': message_json}

    return JsonResponse(result, safe=False)


def get_conversation_users(request, conversation_pk):
    try:
        conversation = Conversation.objects.get(pk=conversation_pk)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

    users = conversation.participants.all()
    users_serialized = serializers.serialize('json', users)
    users_json = json.loads(users_serialized)

    return JsonResponse(users_json, safe=False)


def create_conversation_message(request, conversation_pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Please login first'}, status=401)

    try:
        conversation = Conversation.objects.get(pk=conversation_pk)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

    if request.method == 'POST':
        try:
            message_content = \
                json.loads(request.body.decode('utf-8'))['content']

            new_message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=message_content)

            new_message_qs = conversation.message_set.filter(pk=new_message.pk)
            message_serialized = serializers.serialize('json', new_message_qs)
            message_json = json.loads(message_serialized)

            result = {'newMessage': message_json}
            return JsonResponse(result)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        # return message pk
        return JsonResponse({'message': 'POST request received'})
    else:
        return JsonResponse(
            {'message': 'This view supports POST requests only'}, status=405)



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
