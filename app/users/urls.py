from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('',
         views.users_root,
         name='users_root'),
    path('me/',
         views.UserDetailView.as_view(),
         name='user_detail'),
    path('me/settings/',
         views.user_detail_redirect,
         name='user_detail_redirect'),
    path('me/settings/timezone/',
         views.UserUpdateTimezoneView.as_view(),
         name='user_update_timezone'),
    path('register/',
         views.UserRegisterView.as_view(),
         name='register'),
    path('login/',
         views.UserLoginView.as_view(),
         name='login'),
    path('logout/',
         views.UserLogoutView.as_view(),
         name='logout'),
]
