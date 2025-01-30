from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
import os

from .conversation_models import Conversation
from .group_models import GroupChat
from admin_panel.models import DynamicConfig
from payments.tier_logic import check_user_storage_quota
from accounts.models import UserBlock

class EphemeralMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, null=True, blank=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True, related_name='messages')

    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to='voice_messages/', blank=True, null=True, help_text="Voice or other file attachment")
    pinned = models.BooleanField(default=False)
    one_time_view = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # BLOCK check (recipient blocks sender)
        if self.recipient and UserBlock.objects.filter(blocker=self.recipient, blocked=self.sender).exists():
            raise ValueError(f"Message blocked by recipient {self.recipient.username}")

        # ephemeral timer logic
        if not self.expires_at:
            conv_timer = None
            # check conversation custom timer
            if self.conversation and self.conversation.custom_timer:
                conv_timer = self.conversation.custom_timer
            else:
                # fallback to global default
                gdt = DynamicConfig.objects.filter(key='global_default_timer').first()
                if gdt:
                    try:
                        conv_timer = int(gdt.value)
                    except ValueError:
                        conv_timer = 60
                else:
                    conv_timer = 60
            self.expires_at = timezone.now() + timezone.timedelta(minutes=conv_timer)

        super().save(*args, **kwargs)

        # check storage
        if self.attachment:
            try:
                check_user_storage_quota(self.sender)
            except ValueError:
                # revert
                super().delete()
                raise

    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at

    def __str__(self):
        if self.group:
            return f"[Group: {self.group.name}] {self.sender.username}: {self.content}"
        elif self.conversation:
            return f"[Conv #{self.conversation.id}] {self.sender.username}: {self.content}"
        else:
            return f"{self.sender.username} -> {self.recipient.username}: {self.content}"

class VaultItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=20)  # 'note','password','media','contact'
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    timer = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        return self.timer and timezone.now() > self.timer

    def __str__(self):
        return f"{self.item_type} for {self.user.username}"

class ShareLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vault_item = models.ForeignKey(VaultItem, on_delete=models.CASCADE, null=True, blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    expires_on = models.DateTimeField(null=True, blank=True)
    max_views = models.PositiveIntegerField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        now = timezone.now()
        if self.expires_on and now > self.expires_on:
            return True
        if self.max_views and self.view_count >= self.max_views:
            return True
        return False

    def __str__(self):
        return f"ShareLink {self.token} - {self.is_active}"
