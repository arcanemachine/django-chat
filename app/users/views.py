from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy

from . import forms
from chat.models import Conversation


def users_root(request):
    return HttpResponseRedirect(reverse('users:user_detail'))


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = forms.ChatUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy(settings.LOGIN_URL)
    success_message = "You have successfully registered your account."

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse(self.success_url))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        self.object.profile.timezone = form.cleaned_data['timezone']
        return super().form_valid(form)


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_message = "You are now logged in."


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'users/user_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'profile') \
                and request.user.profile.unread_messages:
            messages.info(self.request, "You have unread messages.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        unread_messages = {}
        for pk in self.request.user.profile.unread_messages:
            unread_messages.update({
                Conversation.objects.get(pk=pk).subject: pk})

        context['unread_messages'] = unread_messages
        return context

    def get_object(self):
        return self.request.user


def user_detail_redirect(request):
    return HttpResponseRedirect(reverse('users:user_detail'))


class UserUpdateTimezoneView(
        LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    fields = ['timezone']
    template_name = 'users/user_update_timezone.html'
    success_message = "Your timezone settings have been updated."

    def get_object(self):
        return self.request.user.profile


class UserLogoutView(LogoutView):
    success_message = "You have successfully logged out."

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
