from django.contrib import admin
from .models import SupportTicket, SupportReply

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('user','subject','status','created_on','updated_on')

@admin.register(SupportReply)
class SupportReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket','staff_member','created_on')
