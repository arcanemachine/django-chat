from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('messages/<int:message_pk>/',
         views.MessageDetail.as_view(),
         name='message_detail'),
]
