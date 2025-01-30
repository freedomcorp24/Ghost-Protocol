from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, TOTPDevice
from .device_models import UserDevice

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','public_name']

class MasterAdminUserAdmin(UserAdmin):
    """
    Only 'masteradmin' can create or remove superusers/staff.
    Integrates 'public_name', 'decoy_password', etc.
    """
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('username','email','public_name','is_staff','is_superuser','is_support','has_2fa','has_duress_enabled')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username','password','email','public_name','decoy_password','has_duress_enabled','recovery_key_hashed')}),
        ('Personal info', {'fields': ('first_name','last_name')}),
        ('Permissions', {'fields': ('is_support','is_active','groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.username != 'masteradmin':
            if 'is_superuser' in form.base_fields:
                form.base_fields.pop('is_superuser')
            if 'is_staff' in form.base_fields:
                form.base_fields.pop('is_staff')
        return form

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # creating a new user
            if request.user.username != 'masteradmin':
                obj.is_staff = False
                obj.is_superuser = False
        else:
            # editing existing
            old_obj = User.objects.get(pk=obj.pk)
            if request.user.username != 'masteradmin':
                obj.is_staff = old_obj.is_staff
                obj.is_superuser = old_obj.is_superuser
        super().save_model(request, obj, form, change)

@admin.register(User)
class UserAdminOverride(MasterAdminUserAdmin):
    pass

@admin.register(TOTPDevice)
class TOTPDeviceAdmin(admin.ModelAdmin):
    list_display = ('user','name','confirmed','created_at')

@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('user','device_id','device_name','platform','created_at','is_wiped')
