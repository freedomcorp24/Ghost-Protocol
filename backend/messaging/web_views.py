from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import EphemeralMessage
from .group_models import GroupChat
from django.utils import timezone

@login_required
def web_chat_page(request):
    # Renders web_chat.html
    return render(request, 'web_chat.html')

@login_required
def web_chat_list(request):
    # Return ephemeral messages (sender/recipient logic)
    msgs = EphemeralMessage.objects.filter(
        recipient=request.user,
        group__isnull=True
    ).order_by('created_at')[:50]
    data = []
    for m in msgs:
        data.append({
            'id': m.id,
            'sender': m.sender.username,
            'content': m.content
        })
    return JsonResponse({'success':True,'messages':data})

@csrf_exempt
@login_required
def web_chat_send(request):
    if request.method=='POST':
        content = request.POST.get('content','')
        m = EphemeralMessage.objects.create(
            sender=request.user,
            recipient=request.user, # or some other recipient logic if needed
            content=content
        )
        return JsonResponse({'success':True,'msg_id':m.id})
    return JsonResponse({'success':False}, status=400)

@login_required
def web_group_chat_page(request):
    return render(request, 'web_group_chat.html')

@login_required
def web_group_list(request, group_id):
    # check membership
    try:
        group = GroupChat.objects.get(id=group_id)
    except GroupChat.DoesNotExist:
        return JsonResponse({'success':False,'message':'No such group'})

    membership = group.groupmembership_set.filter(user=request.user).first()
    if not membership:
        return JsonResponse({'success':False,'message':'You are not in this group'})

    msgs = EphemeralMessage.objects.filter(group=group).order_by('created_at')
    data = []
    for m in msgs:
        data.append({
            'id':m.id,
            'sender': m.sender.username,
            'content': m.content
        })
    return JsonResponse({'success':True,'messages':data})

@csrf_exempt
@login_required
def web_group_send(request, group_id):
    if request.method=='POST':
        content = request.POST.get('content','')
        try:
            group = GroupChat.objects.get(id=group_id)
        except GroupChat.DoesNotExist:
            return JsonResponse({'success':False,'message':'No such group'})
        # check membership
        mem = group.groupmembership_set.filter(user=request.user).first()
        if not mem:
            return JsonResponse({'success':False,'message':'Not in group'})
        msg = EphemeralMessage.objects.create(
            sender=request.user,
            group=group,
            content=content
        )
        return JsonResponse({'success':True,'msg_id': msg.id})
    return JsonResponse({'success':False}, status=400)

@login_required
def web_archived_page(request):
    return render(request, 'web_archived.html')

@login_required
def web_archived_list(request):
    msgs = EphemeralMessage.objects.filter(
        archived=True,
        recipient=request.user
    ).order_by('-created_at')[:50]
    data = []
    for m in msgs:
        data.append({
            'id': m.id,
            'sender': m.sender.username,
            'content': m.content
        })
    return JsonResponse({'success':True,'messages':data})

@csrf_exempt
@login_required
def web_unarchive(request, msg_id):
    if request.method=='POST':
        try:
            msg = EphemeralMessage.objects.get(id=msg_id, recipient=request.user)
            msg.archived = False
            msg.save()
            return JsonResponse({'success':True})
        except EphemeralMessage.DoesNotExist:
            pass
    return JsonResponse({'success':False}, status=400)
