from celery import shared_task
from django.utils import timezone
from django.conf import settings
from .models import EphemeralMessage, VaultItem, ShareLink
from .group_models import GroupChat
from .conversation_models import Conversation
import datetime

@shared_task
def cleanup_ephemeral_data():
    now = timezone.now()

    # ephemeral messages
    msgs = EphemeralMessage.objects.filter(expires_at__isnull=False, expires_at__lt=now)
    count_msg = msgs.count()
    msgs.delete()

    # vault items
    items = VaultItem.objects.filter(timer__isnull=False, timer__lt=now)
    count_items = items.count()
    items.delete()

    # share links
    links = ShareLink.objects.filter(is_active=True)
    deactivated = 0
    for link in links:
        if link.is_expired():
            link.is_active = False
            link.save()
            deactivated += 1

    # ephemeral groups
    ephemeral_groups = GroupChat.objects.filter(is_ephemeral=True)
    for g in ephemeral_groups:
        if g.ephemeral_timer:
            cutoff = now - datetime.timedelta(minutes=g.ephemeral_timer)
            group_msgs = EphemeralMessage.objects.filter(group=g, created_at__lt=cutoff)
            group_msgs.delete()

    # auto-delete old groups if older than a config or settings
    days_str = getattr(settings, 'AUTO_DELETE_OLD_GROUP_DAYS', 90)
    cutoff2 = now - datetime.timedelta(days=int(days_str))
    old_groups = GroupChat.objects.filter(created_at__lt=cutoff2)
    og_count = old_groups.count()
    old_groups.delete()

    return f"Cleaned {count_msg} msgs, {count_items} vault items, {deactivated} links, deleted {og_count} old groups."

@shared_task
def nuke_all_ephemeral():
    """
    'Panic button' that kills ephemeral data across the entire system.
    """
    msg_count = EphemeralMessage.objects.count()
    EphemeralMessage.objects.all().delete()

    vault_count = VaultItem.objects.count()
    VaultItem.objects.all().delete()

    link_count = ShareLink.objects.count()
    ShareLink.objects.all().delete()

    grp_count = GroupChat.objects.count()
    GroupChat.objects.all().delete()

    conv_count = Conversation.objects.count()
    Conversation.objects.all().delete()

    return f"NUKED: {msg_count} messages, {vault_count} vault items, {link_count} share links, {grp_count} groupchats, {conv_count} conversations."
