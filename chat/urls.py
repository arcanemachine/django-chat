from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('',
         views.chat_root,
         name="chat_root"),

    # api helpers
    path('api/urls/reverse/<str:reverse_string>/',
         views.json_reverse_url,
         name='json_reverse_url'),
    path('api/test/hello-world/',
         views.json_hello_world,
         name='json_hello_world'),
    path('api/test/user-is-logged-in/',
         views.json_user_is_logged_in,
         name='json_user_is_logged_in'),
    path('api/test/debug/',
         views.json_debug,
         name='json_debug'),

    path('api/conversations/<int:conversation_pk>/messages/create/',
         views.create_conversation_message,
         name='create_conversation_message'),
    path('api/conversations/<int:conversation_pk>/message/<int:message_pk>/',
         views.get_conversation_message,
         name='get_conversation_message'),
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
