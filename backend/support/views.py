from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import SupportTicket, SupportReply

@login_required
def ticket_list(request):
    if request.user.is_staff or request.user.is_support:
        tickets = SupportTicket.objects.all().order_by('-updated_on')
    else:
        tickets = SupportTicket.objects.filter(user=request.user).order_by('-updated_on')
    return render(request, 'support/ticket_list.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        SupportTicket.objects.create(
            user=request.user,
            subject=subject,
            body=body,
            status='open'
        )
        return redirect('support:ticket_list')
    return render(request, 'support/create_ticket.html')

@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    if not request.user.is_staff and not request.user.is_support and ticket.user != request.user:
        return render(request, 'support/error.html', {'error': "No access to this ticket."})
    replies = ticket.replies.all().order_by('created_on')
    return render(request, 'support/view_ticket.html', {'ticket': ticket, 'replies': replies})

@login_required
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    if ticket.user != request.user and not request.user.is_staff and not request.user.is_support:
        return render(request, 'support/error.html', {'error': "No permission to close."})
    ticket.status = 'closed'
    ticket.closed_on = timezone.now()
    ticket.save()
    return redirect('support:ticket_list')

@login_required
def reopen_ticket(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    if ticket.user != request.user and not request.user.is_staff and not request.user.is_support:
        return render(request, 'support/error.html', {'error': "No permission to reopen."})
    ticket.status = 'open'
    ticket.closed_on = None
    ticket.save()
    return redirect('support:ticket_list')

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    if ticket.user != request.user and not (request.user.is_staff or request.user.is_support):
        return render(request, 'support/error.html', {'error': "No permission to delete."})
    if request.method == 'POST':
        ticket.delete()
        return redirect('support:ticket_list')
    return render(request, 'support/confirm_delete.html', {'ticket': ticket})

@user_passes_test(lambda u: u.is_staff or u.is_support)
def staff_reply(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    if request.method == 'POST':
        reply_text = request.POST.get('reply')
        SupportReply.objects.create(
            ticket=ticket,
            staff_member=request.user,
            reply=reply_text
        )
        ticket.status = 'in_progress'
        ticket.save()
        return redirect('support:view_ticket', ticket_id=ticket_id)
    return render(request, 'support/reply_form.html', {'ticket': ticket})

@user_passes_test(lambda u: u.is_staff or u.is_support)
def escalate_ticket(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    ticket.status = 'escalated'
    ticket.save()
    return redirect('support:view_ticket', ticket_id=ticket_id)
