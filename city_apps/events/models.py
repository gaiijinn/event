from django.db import models

from city_apps.custom_user.models import User


class EventTypes(models.Model):
    event_type = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"{self.event_type}"


class Events(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=128)
    event_descr = models.CharField(max_length=256, null=True, blank=True)
    event_type = models.ForeignKey(to=EventTypes, on_delete=models.CASCADE)
    event_address = models.CharField(max_length=128, null=True, blank=True)
    date = models.DateField()
    begin_time = models.TimeField()
    end_time = models.TimeField()
    event_main_photo = models.ImageField(upload_to='users/events', blank=True)
    additional_event_photo = models.ImageField(upload_to='users/events', blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    coordinates = models.JSONField(null=True, blank=True)

    guests = models.ManyToManyField(User, through='EventGuests', related_name='user_events')


class EventGuests(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    event = models.ForeignKey(to=Events, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event.event_type} - {self.user.email}"
