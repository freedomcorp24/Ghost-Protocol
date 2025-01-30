from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import EphemeralMessage, VaultItem, ShareLink
from .group_models import GroupChat, GroupMembership
from .conversation_models import Conversation
from .link_sharing import validate_share_link

@login_required
def messaging_home(request):
    inbound = EphemeralMessage.objects.filter(recipient=request.user, archived=False).order_by('-created_at')[:50]
    outbound = EphemeralMessage.objects.filter(sender=request.user, archived=False).order_by('-created_at')[:50]
    decoy_mode = request.session.get('decoy_mode', False)
    if decoy_mode:
        inbound = []
        outbound = []
    return render(request, 'messaging/home.html', {'inbound': inbound, 'outbound': outbound, 'decoy_mode': decoy_mode})

@login_required
def group_chat_view(request, group_id):
    group = get_object_or_404(GroupChat, id=group_id)
    membership = GroupMembership.objects.filter(group=group, user=request.user).first()
    if not membership:
        return HttpResponse("Not a member of this group.", status=403)
    msgs = EphemeralMessage.objects.filter(group=group, archived=False).order_by('created_at')
    if request.session.get('decoy_mode', False):
        msgs = []
    return render(request, 'messaging/group_chat.html', {'group': group, 'messages': msgs})

@login_required
def vault_dashboard(request):
    items = VaultItem.objects.filter(user=request.user).order_by('-created_at')
    if request.session.get('decoy_mode', False):
        items = []
    return render(request, 'messaging/vault.html', {'items': items})

def access_share_link(request, token):
    password = request.POST.get('password', None)
    link, error = validate_share_link(token, password=password)
    if error:
        return HttpResponse(error, status=400)
    if not link:
        return HttpResponse("Link invalid or inactive", status=404)
    item = link.vault_item
    return HttpResponse(f"VaultItem: {item.item_type} => {item.data}")

@login_required
def destroy_entire_chat(request, user_id):
    EphemeralMessage.objects.filter(sender=request.user, recipient_id=user_id).delete()
    EphemeralMessage.objects.filter(sender_id=user_id, recipient=request.user).delete()
    return redirect('messaging:home')

@login_required
def one_time_view_media(request, msg_id):
    msg = get_object_or_404(EphemeralMessage, id=msg_id, recipient=request.user)
    if msg.one_time_view and not msg.viewed:
        content = msg.content
        msg.viewed = True
        msg.save()
        return HttpResponse(f"One-time view media: {content}")
    else:
        return HttpResponse("Media not available", status=404)

@login_required
def archive_message(request, msg_id):
    msg = get_object_or_404(EphemeralMessage, id=msg_id)
    if msg.sender != request.user and msg.recipient != request.user:
        return HttpResponse("No permission to archive.", status=403)
    msg.archived = True
    msg.save()
    return redirect('messaging:home')

@login_required
def unarchive_message(request, msg_id):
    msg = get_object_or_404(EphemeralMessage, id=msg_id)
    if msg.sender != request.user and msg.recipient != request.user:
        return HttpResponse("No permission to unarchive.", status=403)
    msg.archived = False
    msg.save()
    return redirect('messaging:home')

@login_required
def archived_unread_count(request):
    count = EphemeralMessage.objects.filter(
        recipient=request.user,
        archived=True,
        viewed=False
    ).count()
    return JsonResponse({'success': True, 'count': count})
