from django.apps import AppConfig


class VisasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.visas'


class VisasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.visas'

    def ready(self):
        import apps.visas.signals 