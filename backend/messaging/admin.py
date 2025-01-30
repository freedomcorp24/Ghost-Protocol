from django.contrib import admin
from .models import EphemeralMessage, VaultItem, ShareLink
from .group_models import GroupChat, GroupMembership
from .conversation_models import Conversation

@admin.register(EphemeralMessage)
class EphemeralMessageAdmin(admin.ModelAdmin):
    list_display = ('sender','recipient','group','conversation','archived','one_time_view','created_at','expires_at')

@admin.register(VaultItem)
class VaultItemAdmin(admin.ModelAdmin):
    list_display = ('user','item_type','created_at','timer')

@admin.register(ShareLink)
class ShareLinkAdmin(admin.ModelAdmin):
    list_display = ('user','vault_item','token','is_active','expires_on')

@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ('name','creator','created_at','is_ephemeral','ephemeral_timer')

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('group','user','role','joined_at')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id','created_at','archived_by_display','is_group_conversation','group')

    def archived_by_display(self, obj):
        """
        Show which users have archived the conversation (if any).
        """
        return ", ".join(u.username for u in obj.archived_by.all())
    archived_by_display.short_description = "Archived By"
