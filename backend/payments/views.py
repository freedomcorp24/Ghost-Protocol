from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SubscriptionTier, PaymentTransaction
import uuid

@login_required
def subscribe_view(request, tier_id):
    tier = get_object_or_404(SubscriptionTier, id=tier_id, is_active=True)
    if request.method == 'POST':
        currency = request.POST.get('currency','BTC')
        return redirect('payments:create_payment', tier_id=tier.id)
    return render(request, 'payments/subscribe.html', {'tier': tier})

@login_required
def create_payment(request, tier_id):
    tier = get_object_or_404(SubscriptionTier, id=tier_id, is_active=True)
    if request.method == 'POST':
        currency = request.POST.get('currency','BTC')
        amount = request.POST.get('amount','0.00')
        tx_id = request.POST.get('tx_id', str(uuid.uuid4())[:16])
        PaymentTransaction.objects.create(
            user=request.user,
            currency=currency,
            amount=amount,
            tx_id=tx_id,
            subscription_tier=tier
        )
        return redirect('payments:payment_thanks')
    return render(request, 'payments/create_payment.html', {'tier': tier})

@login_required
def payment_thanks(request):
    return render(request, 'payments/payment_thanks.html')
