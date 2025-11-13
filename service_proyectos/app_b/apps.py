from django.apps import AppConfig


class AppAConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_b'

    def ready(self):
        from .kafka_consumer import start_consumer
        from .kafka_empresa_cache import start_empresa_cache_listener
        start_consumer()
        start_empresa_cache_listener()
