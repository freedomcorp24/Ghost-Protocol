from django.apps import AppConfig

class MessagingConfig(AppConfig):
    name = 'messaging'
    verbose_name = 'Ephemeral Messaging & Vault'

    def ready(self):
        pass
