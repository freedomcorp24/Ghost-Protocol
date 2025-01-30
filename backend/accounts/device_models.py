from django.db import models
from django.conf import settings

class UserDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=200, unique=True)
    device_name = models.CharField(max_length=200, blank=True)
    platform = models.CharField(max_length=50, blank=True)
    last_active = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_wiped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.device_name} ({self.platform})"
