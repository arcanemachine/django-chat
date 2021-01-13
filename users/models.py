from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    unread_messages = models.JSONField(default=dict)

    def __str__(self):
        return f"user '{self.user.username}'"
