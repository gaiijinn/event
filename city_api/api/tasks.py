from cityMap.celery import app
from .service import successful_entry
from city_apps.events.models import EventGuests, Events


@app.task()
def task_successful_entry(event_id):
    event = EventGuests.objects.select_related('user', 'event').get(id=event_id)
    successful_entry(event)
