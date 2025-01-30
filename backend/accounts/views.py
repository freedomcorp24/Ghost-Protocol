from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import UserRegisterForm, TOTPConfirmForm, DuressSetupForm, RecoveryKeyConfirmForm
from .models import User, TOTPDevice
from .totp_flow import generate_random_secret, verify_token
from .device_models import UserDevice
import os
import base64

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_key = base64.b32encode(os.urandom(20)).decode('utf-8').replace('=', '')
            user.set_recovery_key(raw_key)
            user.save()
            login(request, user)
            return render(request, 'accounts/show_recovery_key.html', {'recovery_key': raw_key})
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_check = User.objects.filter(username=username).first()

        if user_check and user_check.decoy_password and password == user_check.decoy_password:
            # decoy mode
            request.session['decoy_mode'] = True
            login(request, user_check, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('messaging:home')
        else:
            user_auth = authenticate(request, username=username, password=password)
            if user_auth:
                request.session['decoy_mode'] = False
                login(request, user_auth)
                return redirect('messaging:home')
            else:
                return render(request, 'accounts/login.html', {'error': "Invalid credentials"})
    return render(request, 'accounts/login.html')

@login_required
def setup_2fa(request):
    existing_device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()
    if not existing_device:
        secret = generate_random_secret()
        existing_device = TOTPDevice.objects.create(user=request.user, secret_key=secret, confirmed=False)

    uri = f"otpauth://totp/GhostProtocol:{request.user.username}?secret={existing_device.secret_key}&issuer=GhostProtocol"
    return render(request, 'accounts/setup_2fa.html', {
        'secret_key': existing_device.secret_key,
        'otpauth_uri': uri
    })

@login_required
def confirm_2fa(request):
    if request.method == 'POST':
        form = TOTPConfirmForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            device = TOTPDevice.objects.filter(user=request.user, confirmed=False).last()
            if device and verify_token(device.secret_key, token):
                device.confirmed = True
                device.save()
                return redirect('messaging:home')
            else:
                form.add_error('token', "Invalid token.")
    else:
        form = TOTPConfirmForm()
    return render(request, 'accounts/confirm_2fa.html', {'form': form})

@login_required
def setup_duress(request):
    if request.method == 'POST':
        form = DuressSetupForm(request.POST)
        if form.is_valid():
            dp = form.cleaned_data['decoy_password']
            request.user.decoy_password = dp
            request.user.has_duress_enabled = True
            request.user.save()
            return redirect('messaging:home')
    else:
        form = DuressSetupForm()
    return render(request, 'accounts/setup_duress.html', {'form': form})

def reset_password_via_recovery(request):
    if request.method == 'POST':
        form = RecoveryKeyConfirmForm(request.POST)
        if form.is_valid():
            rec_key = form.cleaned_data['recovery_key']
            new_pass = form.cleaned_data['new_password']
            # example approach: check all users that have a hashed key
            possible_users = User.objects.exclude(recovery_key_hashed__isnull=True)
            for usr in possible_users:
                if usr.check_recovery_key(rec_key):
                    usr.set_password(new_pass)
                    usr.save()
                    return redirect('accounts:login')
            form.add_error('recovery_key', "Invalid or not found among users.")
    else:
        form = RecoveryKeyConfirmForm()
    return render(request, 'accounts/reset_via_recovery.html', {'form': form})

@login_required
def device_management(request):
    devices = UserDevice.objects.filter(user=request.user)
    return render(request, 'accounts/device_list.html', {'devices': devices})

@login_required
def remote_wipe_device(request, device_id):
    dev = get_object_or_404(UserDevice, device_id=device_id, user=request.user)
    dev.is_wiped = True
    dev.save()
    return redirect('accounts:device_management')
