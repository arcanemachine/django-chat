from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from django_chat import views as project_views


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
@user_passes_test(is_staff)
def chat_conversation_view(request):
    return render(request, 'jasmine/chat_conversation_view.html')


# experiments
@user_passes_test(is_staff)
def hello_include(request):
    """
    Test ability to return other Django views.
    """
    return project_views.root(request)
