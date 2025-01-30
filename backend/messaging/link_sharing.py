from .models import ShareLink
from django.utils import timezone

def validate_share_link(token, password=None):
    try:
        link = ShareLink.objects.get(token=token, is_active=True)
    except ShareLink.DoesNotExist:
        return None, "Link not found or inactive"

    if link.is_expired():
        link.is_active = False
        link.save()
        return None, "Link expired"

    if link.password and password != link.password:
        return None, "Incorrect password"

    if link.max_views:
        link.view_count += 1
        link.save()
        if link.is_expired():
            link.is_active = False
            link.save()
            return None, "Link expired after this view"

    return link, None
