from django.http import HttpResponseRedirect
from django.urls import reverse


def root(request):
    return HttpResponseRedirect(reverse('chat:chat_root'))
