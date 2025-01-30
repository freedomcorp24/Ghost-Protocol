from django.apps import AppConfig

class PaymentsConfig(AppConfig):
    name = 'payments'
    verbose_name = 'Subscription & Payment Logic'

    def ready(self):
        pass
