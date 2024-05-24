from django.apps import AppConfig


class CustomUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'city_apps.custom_user'

    def ready(self):
        import city_apps.custom_user.signals