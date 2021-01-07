from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

UserModel = get_user_model()


class Conversation(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_by',
        on_delete=models.SET_NULL,
        null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name='send to')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.pk} - {self.subject}"

    def get_absolute_url(self):
        return reverse(
            'chat:conversation_view', kwargs={'conversation_pk': self.pk})


class Message(models.Model):
    conversation = \
        models.ForeignKey('Conversation', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    sender_username = models.CharField(max_length=150, default='')
    content = models.TextField("Message Content")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    def get_absolute_url(self):
        return reverse(
            'chat:conversation_view', kwargs={
                'conversation_pk': self.conversation.pk})

    def save(self, *args, **kwargs):
        if not self.sender_username:
            self.sender_username = self.sender.username
        super().save(*args, **kwargs)
