from django.apps import AppConfig


class CommunicationConfig(AppConfig):
    name = 'communication'

    def ready(self):
        from communication import signals  # noqa: F401
