from django.db import models
from django.conf import settings
from django.utils import timezone

class CallSession(models.Model):
    """
    Minimal model to track ongoing calls, 1-on-1 or group.
    We store a random session_id that clients use for signaling.
    """
    session_id = models.CharField(max_length=100, unique=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_calls')
    is_group_call = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CallSession {self.session_id} by {self.creator.username}"
