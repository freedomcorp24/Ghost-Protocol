from django.contrib import admin
from .models import FlaggedAccount, DynamicConfig

@admin.register(FlaggedAccount)
class FlaggedAccountAdmin(admin.ModelAdmin):
    list_display = ('user','reason','flagged_on','resolved')

@admin.register(DynamicConfig)
class DynamicConfigAdmin(admin.ModelAdmin):
    list_display = ('key','value','updated_at')
