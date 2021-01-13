from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Message


@receiver(post_save, sender=Message)
def new_message_notify_conversation_participants(sender, instance, **kwargs):
    """
    When a new message is saved, change unread_messages for other participants.
    """
    if instance.created_at + timezone.timedelta(seconds=5) \
            > instance.modified_at:
        for user in instance.conversation.participants.all():
            if user != instance.sender and str(instance.conversation.pk) \
                    not in user.profile.unread_messages:
                user.profile.unread_messages.update({
                    f'{str(instance.conversation.pk)}': instance.pk})
                user.profile.save()
