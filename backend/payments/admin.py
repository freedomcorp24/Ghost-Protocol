from django.contrib import admin
from .models import SubscriptionTier, UserSubscription, PaymentTransaction

@admin.register(SubscriptionTier)
class SubscriptionTierAdmin(admin.ModelAdmin):
    list_display = ('name','storage_gb','monthly_price_eur','annual_price_eur','is_active')

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user','tier','start_date','end_date','is_active')

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user','currency','amount','tx_id','status','created_on','subscription_tier')
