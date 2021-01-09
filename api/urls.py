from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    #path('conversations/<int:conversation_pk>/',
    #     views.MessageCreate.as_view(),
    #     name='message_create'),
    path('', views.hello_world, name='hello_world'),
    path('conversations/<int:conversation_pk>/messages/',
         views.MessageList.as_view(),
         name='message_list'),
    path('conversations/<int:conversation_pk>/messages/count/'
         '<int:message_count>/',
         views.MessageListCount.as_view(),
         name='message_list_count'),
    path('conversations/<int:conversation_pk>/messages/list-create/',
         views.MessageListCreate.as_view(),
         name='message_list_create'),
    path('conversations/<int:conversation_pk>/messages/range/'
         '<int:range_from>/<int:range_to>/',
         views.MessageListRange.as_view(),
         name='message_list_range'),
    path('messages/<int:message_pk>/',
         views.MessageDetail.as_view(),
         name='message_detail'),
]
