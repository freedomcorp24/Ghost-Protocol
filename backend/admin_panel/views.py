from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .models import FlaggedAccount, DynamicConfig
from messaging.models import EphemeralMessage, VaultItem, ShareLink
from messaging.group_models import GroupChat, GroupMembership
from messaging.conversation_models import Conversation
from payments.models import SubscriptionTier, UserSubscription
from django import forms
import datetime

def admin_check(user):
    return user.is_staff or user.is_superuser

@user_passes_test(admin_check)
def flagged_accounts_list(request):
    flags = FlaggedAccount.objects.filter(resolved=False)
    return render(request, 'admin_panel/flagged_list.html', {'flags': flags})

@user_passes_test(admin_check)
def resolve_flag(request, flag_id):
    flag = get_object_or_404(FlaggedAccount, id=flag_id)
    flag.resolved = True
    flag.save()
    return redirect('admin_panel:flagged_accounts')

@user_passes_test(admin_check)
def dynamic_config_list(request):
    configs = DynamicConfig.objects.all()
    return render(request, 'admin_panel/dynamic_config_list.html', {'configs': configs})

@user_passes_test(admin_check)
def edit_config(request, config_id):
    dc = get_object_or_404(DynamicConfig, id=config_id)
    if request.method == 'POST':
        new_value = request.POST.get('value')
        dc.value = new_value
        dc.updated_at = timezone.now()
        dc.save()
        return redirect('admin_panel:dynamic_config')
    return render(request, 'admin_panel/edit_config.html', {'dc': dc})

@user_passes_test(admin_check)
def share_links_list(request):
    links = ShareLink.objects.filter(is_active=True)
    return render(request, 'admin_panel/links_list.html', {'links': links})

@user_passes_test(admin_check)
def remove_share_link(request, token):
    link = get_object_or_404(ShareLink, token=token, is_active=True)
    link.is_active = False
    link.save()
    return redirect('admin_panel:share_links')

class TierForm(forms.ModelForm):
    class Meta:
        model = SubscriptionTier
        fields = ['name','storage_gb','monthly_price_eur','annual_price_eur','is_active']

@user_passes_test(admin_check)
def tier_list(request):
    tiers = SubscriptionTier.objects.all().order_by('storage_gb')
    return render(request, 'admin_panel/tier_list.html', {'tiers': tiers})

@user_passes_test(admin_check)
def add_tier(request):
    if request.method == 'POST':
        form = TierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:tier_list')
    else:
        form = TierForm()
    return render(request, 'admin_panel/tier_form.html', {'form': form, 'action':'Add Tier'})

@user_passes_test(admin_check)
def edit_tier(request, tier_id):
    tier = get_object_or_404(SubscriptionTier, id=tier_id)
    if request.method == 'POST':
        form = TierForm(request.POST, instance=tier)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:tier_list')
    else:
        form = TierForm(instance=tier)
    return render(request, 'admin_panel/tier_form.html', {'form': form, 'action':'Edit Tier'})

@user_passes_test(admin_check)
def delete_tier(request, tier_id):
    tier = get_object_or_404(SubscriptionTier, id=tier_id)
    if request.method == 'POST':
        tier.is_active = False
        tier.save()
        return redirect('admin_panel:tier_list')
    return render(request, 'admin_panel/confirm_delete_tier.html', {'tier':tier})

@user_passes_test(admin_check)
def nuke_all_data(request):
    """
    Wipe ephemeral messages, vault items, share links, groups, conversations, etc.
    """
    if request.method == 'POST':
        msg_count = EphemeralMessage.objects.count()
        vault_count = VaultItem.objects.count()
        link_count = ShareLink.objects.count()
        grp_count = GroupChat.objects.count()
        conv_count = Conversation.objects.count()

        EphemeralMessage.objects.all().delete()
        VaultItem.objects.all().delete()
        ShareLink.objects.all().delete()
        GroupMembership.objects.all().delete()
        GroupChat.objects.all().delete()
        Conversation.objects.all().delete()

        return render(request, 'admin_panel/nuke_result.html', {
            'msg_count': msg_count,
            'vault_count': vault_count,
            'link_count': link_count,
            'grp_count': grp_count,
            'conv_count': conv_count
        })

    return render(request, 'admin_panel/nuke_confirm.html')

# ------------------- NEW: Admin Edit Premium (Extend / Remove) -------------------

@user_passes_test(admin_check)
def extend_user_subscription(request, user_id):
    """
    Admin route to manually add premium days to user #<user_id>.
    """
    from django.contrib.auth import get_user_model
    user = get_object_or_404(get_user_model(), id=user_id)
    # Attempt to get the user's active subscription
    sub = UserSubscription.objects.filter(user=user, is_active=True).last()

    if request.method == 'POST':
        days_str = request.POST.get('days','30')
        try:
            days_to_add = int(days_str)
        except ValueError:
            days_to_add = 30

        # pick any active tier to assign if user has none
        default_tier = SubscriptionTier.objects.filter(is_active=True).first()
        if not sub or not sub.is_active:
            # create new sub
            import datetime
            end = timezone.now() + datetime.timedelta(days=days_to_add)
            UserSubscription.objects.create(user=user, tier=default_tier, end_date=end, is_active=True)
        else:
            # extend
            if sub.end_date and sub.end_date > timezone.now():
                sub.end_date += datetime.timedelta(days=days_to_add)
            else:
                sub.end_date = timezone.now() + datetime.timedelta(days=days_to_add)
            sub.save()
        return render(request, 'admin_panel/extend_sub_result.html', {'user': user, 'days': days_to_add})

    return render(request, 'admin_panel/extend_sub.html', {'user': user})

@user_passes_test(admin_check)
def remove_user_subscription(request, user_id):
    """
    Admin route to remove premium (mark subscription inactive) for user #<user_id>.
    """
    from django.contrib.auth import get_user_model
    user = get_object_or_404(get_user_model(), id=user_id)
    active_subs = UserSubscription.objects.filter(user=user, is_active=True)

    if request.method == 'POST':
        count = active_subs.count()
        for s in active_subs:
            s.is_active = False
            s.save()
        return render(request, 'admin_panel/remove_sub_result.html', {'user': user, 'count': count})

    return render(request, 'admin_panel/remove_sub_confirm.html', {'user': user, 'subs': active_subs})
