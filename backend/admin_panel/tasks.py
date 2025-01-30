from celery import shared_task
from django.utils import timezone
import datetime
from .models import FlaggedAccount

@shared_task
def auto_resolve_flagged():
    cutoff = timezone.now() - datetime.timedelta(days=30)
    old_flags = FlaggedAccount.objects.filter(flagged_on__lt=cutoff, resolved=False)
    count = old_flags.count()
    old_flags.update(resolved=True)
    return f"Auto-resolved {count} flagged accounts older than 30 days."
