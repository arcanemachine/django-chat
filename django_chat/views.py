from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def root(request):
    return HttpResponseRedirect(reverse('chat:chat_root'))


def hello_jasmine(request):
    return render(request, 'jasmine.html')


def boilerplate_vue(request):
    return render(request, 'boilerplate_vue.html')
