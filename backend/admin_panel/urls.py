from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('flagged/', views.flagged_accounts_list, name='flagged_accounts'),
    path('flagged/resolve/<int:flag_id>/', views.resolve_flag, name='resolve_flag'),
    path('dynamic-config/', views.dynamic_config_list, name='dynamic_config'),
    path('dynamic-config/edit/<int:config_id>/', views.edit_config, name='edit_config'),
    path('links/', views.share_links_list, name='share_links'),
    path('links/remove/<uuid:token>/', views.remove_share_link, name='remove_share_link'),

    path('tiers/', views.tier_list, name='tier_list'),
    path('tiers/add/', views.add_tier, name='add_tier'),
    path('tiers/edit/<int:tier_id>/', views.edit_tier, name='edit_tier'),
    path('tiers/delete/<int:tier_id>/', views.delete_tier, name='delete_tier'),

    path('nuke/', views.nuke_all_data, name='nuke_data'),  # entire self-destruct

    # NEW: admin manually extend/remove user subscription
    path('subscription/extend/<int:user_id>/', views.extend_user_subscription, name='extend_user_sub'),
    path('subscription/remove/<int:user_id>/', views.remove_user_subscription, name='remove_user_sub'),
]
