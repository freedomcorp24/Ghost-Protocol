# ghost_protocol/backend/accounts/web_block_views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import UserBlock, User

@login_required
def web_blocklist_page(request):
    return render(request, 'web_blocklist.html')

@login_required
def web_blocklist(request):
    blocks = UserBlock.objects.filter(blocker=request.user)
    data = []
    for b in blocks:
        data.append({
            'blockId': b.id,
            'blockedName': b.blocked.username,
        })
    return JsonResponse({'success':True,'blocks':data})

@csrf_exempt
@login_required
def web_block_add(request):
    if request.method=='POST':
        blocked_id = request.POST.get('blocked_id')
        try:
            blocked_user = User.objects.get(id=blocked_id)
            ub,created = UserBlock.objects.get_or_create(blocker=request.user, blocked=blocked_user)
            return JsonResponse({'success':True})
        except User.DoesNotExist:
            return JsonResponse({'success':False, 'message':'No such user'})
    return JsonResponse({'success':False}, status=400)

@csrf_exempt
@login_required
def web_block_remove(request):
    if request.method=='POST':
        block_id = request.POST.get('block_id')
        try:
            ub = UserBlock.objects.get(id=block_id, blocker=request.user)
            ub.delete()
            return JsonResponse({'success':True})
        except UserBlock.DoesNotExist:
            return JsonResponse({'success':False, 'message':'No such block'})
    return JsonResponse({'success':False}, status=400)
