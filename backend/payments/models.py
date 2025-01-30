from django.db import models
from django.conf import settings
from django.utils import timezone

class SubscriptionTier(models.Model):
    name = models.CharField(max_length=50, unique=True)
    storage_gb = models.PositiveIntegerField()
    monthly_price_eur = models.DecimalField(max_digits=10, decimal_places=2)
    annual_price_eur = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.storage_gb}GB)"

class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tier = models.ForeignKey(SubscriptionTier, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} on {self.tier.name if self.tier else 'None'}"

class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('failed','Failed'),
    ]
    CURRENCY_CHOICES = [
        ('BTC','Bitcoin'),
        ('XMR','Monero'),
        ('USDT','USDT-TRC20'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    tx_id = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_on = models.DateTimeField(auto_now_add=True)
    subscription_tier = models.ForeignKey(SubscriptionTier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.currency} Tx {self.tx_id} ({self.status})"
