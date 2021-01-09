from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    #path('conversations/<int:conversation_pk>/',
    #     views.MessageCreate.as_view(),
    #     name='message_create'),
    path('', views.hello_world, name='hello_world'),

    # users
    path('users/',
        views.UserList.as_view(),
        name='user_list'),
    path('users/<int:user_pk>/',
        views.UserDetail.as_view(),
        name='user_detail'),

    # conversations
    path('conversations/<int:conversation_pk>/users/',
         views.ConversationUserList.as_view(),
         name='conversation_user_list'),

    # messages
    path('conversations/<int:conversation_pk>/messages/',
         views.MessageList.as_view(),
         name='message_list'),
    path('conversations/<int:conversation_pk>/messages/list-create/',
         views.MessageListCreate.as_view(),
         name='message_list_create'),

    # only shows the last message (less scrolling) # deleteme
    path('conversations/<int:conversation_pk>/messages/list-create-last/',
         views.MessageListCreateLast.as_view(),
         name='message_list_create_last'),

    path('conversations/<int:conversation_pk>/messages/count/'
         '<int:message_count>/',
         views.MessageListCount.as_view(),
         name='message_list_count'),
    path('conversations/<int:conversation_pk>/messages/range/'
         '<int:range_from>/<int:range_to>/',
         views.MessageListRange.as_view(),
         name='message_list_range'),
    path('conversations/<int:conversation_pk>/messages/create/',
         views.MessageCreate.as_view(),
         name='message_create'),
    path('conversations/<int:conversation_pk>/messages/<int:message_pk>/',
         views.MessageDetail.as_view(),
         name='message_detail'),
]
