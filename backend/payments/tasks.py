from celery import shared_task
from django.utils import timezone
from .models import PaymentTransaction, UserSubscription
from .transaction_check import check_crypto_tx
import datetime

@shared_task
def confirm_payments():
    pending_txs = PaymentTransaction.objects.filter(status='pending')
    confirmed_count = 0

    for tx in pending_txs:
        if check_crypto_tx(tx.currency, tx.tx_id):
            tx.status = 'confirmed'
            tx.save()
            sub_tier = tx.subscription_tier
            user_sub = UserSubscription.objects.filter(user=tx.user, is_active=True).last()

            # For simplicity, assume monthly => 30 days
            days_to_add = 30

            if not user_sub or not user_sub.is_active:
                end = timezone.now() + datetime.timedelta(days=days_to_add)
                UserSubscription.objects.create(
                    user=tx.user, tier=sub_tier,
                    end_date=end, is_active=True
                )
            else:
                if user_sub.end_date and user_sub.end_date > timezone.now():
                    user_sub.end_date += datetime.timedelta(days=days_to_add)
                else:
                    user_sub.end_date = timezone.now() + datetime.timedelta(days=days_to_add)
                user_sub.save()
            confirmed_count += 1

    return f"Confirmed {confirmed_count} transactions."
