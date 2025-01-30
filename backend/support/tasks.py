from celery import shared_task
from django.utils import timezone
from .models import SupportTicket
import datetime

@shared_task
def purge_closed_tickets():
    """
    Auto-purge tickets 30 days after closure.
    """
    cutoff = timezone.now() - datetime.timedelta(days=30)
    old_closed = SupportTicket.objects.filter(status='closed', closed_on__lt=cutoff)
    count = old_closed.count()
    old_closed.delete()
    return f"Purged {count} closed support tickets older than 30 days."
