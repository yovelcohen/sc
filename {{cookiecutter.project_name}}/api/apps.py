from django.apps import AppConfig


class ConsumerApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        import api.signals  # noqa
