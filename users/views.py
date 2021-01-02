from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.urls import reverse, reverse_lazy


def users_root(request):
    return HttpResponseRedirect(reverse('users:user_detail'))

class UserRegisterView(CreateView, SuccessMessageMixin):
    form_class = UserCreationForm
    template_name = 'users/user_register.html'
    success_url = reverse_lazy(settings.LOGIN_URL)
    success_message = "You have successfully registered your account."

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse(self.success_url))
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView, SuccessMessageMixin):
    form_class = AuthenticationForm
    template_name = 'users/user_login.html'
    redirect_authenticated_user = True
    success_message = "You are now logged in."


class UserDetailView(DetailView, LoginRequiredMixin):
    template_name = 'users/user_detail.html'
    
    def get_object(self):
        return self.request.user


class UserLogoutView(LogoutView):
    success_message = "You have successfully logged out."

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
