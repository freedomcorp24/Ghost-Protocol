from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from accounts.views import custom_login_view, register_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', custom_login_view, name='login'),
    path('accounts/register/', register_user, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/', include('accounts.urls')),
    path('messaging/', include('messaging.urls')),
    path('payments/', include('payments.urls')),
    path('admin-panel/', include('admin_panel.urls')),
    path('support/', include('support.urls')),
    path('call/', include('call.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
