from django.apps import AppConfig


class AutoparkConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "autopark"

    def ready(self):
        import autopark.signals
