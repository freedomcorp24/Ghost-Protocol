from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = 'Accounts & Authentication'

    def ready(self):
        pass
