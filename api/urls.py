from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    #path('conversations/<int:conversation_pk>/',
    #     views.MessageCreate.as_view(),
    #     name='message_create'),
    path('messages/<int:message_pk>/',
         views.MessageDetail.as_view(),
         name='message_detail'),
]
