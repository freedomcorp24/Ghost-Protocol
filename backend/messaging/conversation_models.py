from django.db import models
from django.conf import settings
from django.utils import timezone
from .group_models import GroupChat

class Conversation(models.Model):
    """
    A high-level conversation model for 1-on-1 or group chat references.
    - participants: for direct chats
    - group: if it's group-based
    - archived_by: which users archived the entire conversation
    - custom_timer: if set, ephemeral messages in this conversation
      default to this timer (in minutes) instead of global default
    """
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='conversations')
    group = models.OneToOneField(GroupChat, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archived_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='archived_conversations')

    custom_timer = models.PositiveIntegerField(null=True, blank=True, help_text="Minutes for conversation-specific ephemeral timer")

    def is_group_conversation(self):
        return self.group is not None

    def __str__(self):
        return f"Conversation #{self.id} (Group? {self.is_group_conversation()})"
