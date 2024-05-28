from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'city_apps.events'

    def ready(self):
        import city_apps.events.signals
