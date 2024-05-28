from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EventGuests, Events


@receiver(post_save, sender=Events)
def set_owner_as_guest(sender, instance, created, **kwargs):
    if created:
        EventGuests.objects.create(user=instance.user, event=instance)
