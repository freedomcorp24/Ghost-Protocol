from django.apps import AppConfig

class SupportConfig(AppConfig):
    name = 'support'
    verbose_name = 'User Support & Ticket System'

    def ready(self):
        pass
