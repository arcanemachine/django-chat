from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('',
         views.chat_root,
         name="chat_root"),

    # deleteme
    path('api/test/',
         views.test_message,
         name='test_message'),
    path('api/conversations/<int:conversation_pk>/messages/'
         '<int:number_of_messages>/',
         views.get_conversation_messages,
         name='get_conversation_messages'),
    path('api/conversations/<int:conversation_pk>/users/',
         views.get_conversation_users,
         name='get_conversation_users'),

    path('conversations/all/',
         views.ConversationListView.as_view(),
         name="conversation_list"),
    path('conversations/new/',
         views.ConversationCreateView.as_view(),
         name="conversation_create"),
    path('conversations/<int:conversation_pk>/',
         views.ConversationView.as_view(),
         name="conversation_view"),
    path('conversations/<int:conversation_pk>/update-participants/',
         views.ConversationUpdateParticipantsView.as_view(),
         name="conversation_update_participants"),

    path('messages/all/',
         views.MessageListView.as_view(),
         name="message_list"),
]
