from django.urls import include, path

from . import views

app_name = 'jasmine'

urlpatterns = [
    path('', views.jasmine_root, name='jasmine_root'),

    # tutorial/practice
    path('hello/', views.hello_jasmine, name='hello_jasmine'),
    path('hello/vue/', views.hello_vue, name='hello_vue'),
    path('hello/vue/t/', views.hello_vue_test, name='hello_vue_test'),

    # experiments
    path('experiments/include/', views.hello_include, name='hello_include'),

    # chat
    path('chat/conversations/',
         views.chat_conversation_view,
         name='chat_conversation_view'),
]
