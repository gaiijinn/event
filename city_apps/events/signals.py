from django.db.models.signals import post_save
from django.dispatch import receiver
from city_api.api.tasks import task_successful_entry
from .models import EventGuests, Events


@receiver(post_save, sender=Events)
def set_owner_as_guest(sender, instance, created, **kwargs):
    if created:
        # тут написать на почту что успешно создано
        EventGuests.objects.create(user=instance.user, event=instance)


@receiver(post_save, sender=EventGuests)
def send_guest_email(sender, instance, created, **kwargs):
    if created:
        task_successful_entry.delay(instance.id)
