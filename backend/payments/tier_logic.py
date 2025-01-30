from .models import SubscriptionTier, UserSubscription
from django.utils import timezone
from messaging.models import EphemeralMessage, VaultItem
import os

def get_user_quota_in_gb(user):
    sub = UserSubscription.objects.filter(user=user, is_active=True).last()
    if not sub or not sub.tier:
        return 0
    return sub.tier.storage_gb

def is_sub_active(user):
    sub = UserSubscription.objects.filter(user=user, is_active=True).last()
    if not sub:
        return False
    if sub.end_date and timezone.now() > sub.end_date:
        return False
    return True

def check_user_storage_quota(user):
    """
    Sums ephemeral attachments (like voice) + any other local file usage.
    In a real system with S3, you'd do a different approach for file size.
    If total > tier limit, raise ValueError.
    """
    tier_gb = get_user_quota_in_gb(user)
    if tier_gb <= 0:
        # means user has no storage, up to you whether to allow or block
        raise ValueError(f"User {user.username} has 0GB storage tier.")

    tier_bytes = tier_gb * 1024 * 1024 * 1024
    total_size = 0

    # Summation of ephemeral attachments
    ephemeral_attachments = EphemeralMessage.objects.filter(sender=user, attachment__isnull=False)
    for em in ephemeral_attachments:
        if em.attachment and em.attachment.name:
            try:
                file_path = em.attachment.path
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
            except:
                pass

    # If VaultItem also stored local files, sum them up. Currently, we have data as text only.

    if total_size > tier_bytes:
        raise ValueError(f"Storage limit exceeded for user {user.username} (exceeds {tier_gb}GB).")

def grandfather_existing_users(tier):
    # no forced removal from old tier
    pass
