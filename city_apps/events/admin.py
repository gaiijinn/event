from django.contrib import admin

from .models import EventGuests, Events, EventTypes

# Register your models here.

admin.site.register(Events)
admin.site.register(EventGuests)
admin.site.register(EventTypes)
