from django.apps import AppConfig

class AdminPanelConfig(AppConfig):
    name = 'admin_panel'
    verbose_name = 'Ghost Protocol Admin Panel'

    def ready(self):
        pass
