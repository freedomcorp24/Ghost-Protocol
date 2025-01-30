from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib

def hash_recovery_key(key_plain):
    return hashlib.sha256(key_plain.encode('utf-8')).hexdigest()

class User(AbstractUser):
    public_name = models.CharField(max_length=100, blank=True, null=True)
    decoy_password = models.CharField(max_length=128, null=True, blank=True)
    has_duress_enabled = models.BooleanField(default=False)
    recovery_key_hashed = models.CharField(max_length=255, null=True, blank=True)
    is_support = models.BooleanField(default=False)

    @property
    def has_2fa(self):
        return self.totpdevice_set.filter(confirmed=True).exists()

    def set_recovery_key(self, raw_key):
        self.recovery_key_hashed = hash_recovery_key(raw_key)

    def check_recovery_key(self, raw_key):
        return self.recovery_key_hashed == hash_recovery_key(raw_key)

    def __str__(self):
        return self.username

class UserBlock(models.Model):
    """
    For user-level blocking. If 'blocker' blocks 'blocked',
    ephemeral messages from 'blocked' to 'blocker' are disallowed.
    """
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocks_initiated')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker','blocked')

    def __str__(self):
        return f"{self.blocker.username} blocks {self.blocked.username}"
