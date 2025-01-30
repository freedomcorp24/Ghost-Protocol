from django.db import models
from django.conf import settings
from django.utils import timezone

STATUS_CHOICES = [
    ('open','Open'),
    ('in_progress','In Progress'),
    ('escalated','Escalated'),
    ('closed','Closed'),
]

class SupportTicket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    body = models.TextField(max_length=2000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    closed_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} - {self.status}"

class SupportReply(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='replies')
    staff_member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply = models.TextField(max_length=2000)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.staff_member} on {self.ticket.subject}"
