from django.apps import AppConfig

class WagtailAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wagtail_app'

    def ready(self):
        from . import signals  # Import the signals module
