from django.db import models
from django.conf import settings
from django.utils import timezone

class FlaggedAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    flagged_on = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Flagged {self.user.username}: {self.reason}"

class DynamicConfig(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=500)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key} => {self.value}"
