from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.staticfiles import finders
from django.shortcuts import render

from django_chat import views as project_views
from chat import views as chat_views


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def jasmine_root(request):
    """
    Jasmine Test Index
    """
    return render(request, 'jasmine/root.html')


# tutorial/practice #
@user_passes_test(is_staff)
def hello_jasmine(request):
    """
    Basic Jasmine Tests using plain JS.
    """
    return render(request, 'jasmine/hello_jasmine.html')


@user_passes_test(is_staff)
def hello_vue(request):
    """
    Test the ability of Jasmine to interact with a Vue app. (Template)
    """
    return render(request, 'jasmine/hello_vue.html')


@user_passes_test(is_staff)
def hello_vue_test(request):
    """
    Test the ability of Jasmine to interact with a Vue app. (Test)
    """
    return render(request, 'jasmine/hello_vue.html', {'test_jasmine': True})


# chat
class ChatConversationView(chat_views.ConversationView, UserPassesTestMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jasmine_specs'] = [
            finders.find('jasmine/spec/ConversationView.js')]
        return context

    def test_func(self):
        return self.request.user.is_staff


# experiments
@user_passes_test(is_staff)
def hello_include(request):
    """
    Test ability to return other Django views.
    """
    return project_views.root(request)
