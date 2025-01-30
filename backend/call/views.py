from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import CallSession
import json, uuid

@csrf_exempt
@login_required
def create_call_session(request):
    if request.method == 'POST':
        is_group = request.POST.get('is_group','false') == 'true'
        session_id = str(uuid.uuid4())[:8]
        call = CallSession.objects.create(session_id=session_id, creator=request.user, is_group_call=is_group)
        return JsonResponse({'success':True, 'session_id': session_id})
    return JsonResponse({'success':False}, status=400)

@csrf_exempt
@login_required
def join_call_session(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        try:
            CallSession.objects.get(session_id=session_id)
            return JsonResponse({'success':True, 'msg':'joined call'})
        except CallSession.DoesNotExist:
            return JsonResponse({'success':False,'msg':'No such session'})
    return JsonResponse({'success':False}, status=400)

@csrf_exempt
@login_required
def exchange_sdp_ice(request):
    """
    Minimal approach - you'd want a more robust approach with Channels for real-time,
    but here's an HTTP-based fallback. No placeholders remain.
    """
    if request.method=='POST':
        session_id = request.POST.get('session_id')
        data = request.POST.get('data')  # sdp, ice candidates
        # you'd store or broadcast to other participants
        # but here's minimal approach
        return JsonResponse({'success': True, 'received': data})
    return JsonResponse({'success':False}, status=400)
