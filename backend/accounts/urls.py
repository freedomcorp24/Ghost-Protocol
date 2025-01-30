from django.urls import path
from . import views
from . import web_block_views  # new for blocklist web endpoints

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('2fa/setup/', views.setup_2fa, name='setup_2fa'),
    path('2fa/confirm/', views.confirm_2fa, name='confirm_2fa'),
    path('duress/setup/', views.setup_duress, name='setup_duress'),
    path('recovery/reset/', views.reset_password_via_recovery, name='reset_via_recovery'),
    path('devices/', views.device_management, name='device_management'),
    path('devices/wipe/<str:device_id>/', views.remote_wipe_device, name='remote_wipe_device'),

    # Web blocklist endpoints
    path('webBlockList', web_block_views.web_blocklist, name='webBlockList'),
    path('webBlockAdd', web_block_views.web_block_add, name='webBlockAdd'),
    path('webBlockRemove', web_block_views.web_block_remove, name='webBlockRemove'),
    path('webBlocklist', web_block_views.web_blocklist_page, name='web_blocklist'),
]
