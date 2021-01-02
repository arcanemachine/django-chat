from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('',
         views.chat_root,
         name="chat_root"),

    path('conversations/all/',
         views.ConversationListView.as_view(),
         name="conversation_list"),
    path('conversations/new/',
         views.ConversationCreateView.as_view(),
         name="conversation_create"),
    path('conversations/<pk>/',
         views.ConversationView.as_view(),
         name="conversation_view"),

    path('messages/all/',
         views.MessageListView.as_view(),
         name="message_list"),
]
