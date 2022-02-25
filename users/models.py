from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from timezone_field import TimeZoneField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    timezone = TimeZoneField(
        default='Canada/Mountain', choices_display="WITH_GMT_OFFSET")

    unread_messages = models.JSONField(default=dict)

    def __str__(self):
        return f"user '{self.user.username}'"

    def get_absolute_url(self):
        return self.user.get_absolute_url()

    def get_localized_timestamp(self, timestamp=None):
        if timestamp is None:
            timestamp = timezone.datetime.now()
        return timestamp.astimezone(self.timezone)

    def get_timezone_offset(self, milliseconds=True, seconds=False,
                            minutes=False, hours=False):
        result = self.timezone.utcoffset(timezone.datetime.now())
        if hours is True:
            return result.total_seconds() / 3600
        elif minutes is True:
            return result.total_seconds() / 60
        elif seconds is True:
            return result.total_seconds()
        return result.total_seconds() * 1000

    def get_timezone_abbreviation(self, timestamp=None):
        if timestamp is None:
            timestamp = self.get_localized_timestamp()
        return timestamp.tzname()
