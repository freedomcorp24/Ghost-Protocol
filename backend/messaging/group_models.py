from django.db import models
from django.conf import settings

class GroupChat(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    is_ephemeral = models.BooleanField(default=False)
    ephemeral_timer = models.PositiveIntegerField(null=True, blank=True, help_text="Minutes for auto-delete")

    def __str__(self):
        return f"GroupChat: {self.name}"

class GroupMembership(models.Model):
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.group.name} as {self.role}"
