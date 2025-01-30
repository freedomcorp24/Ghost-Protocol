from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','public_name']

class TOTPConfirmForm(forms.Form):
    token = forms.CharField(label="TOTP Token", max_length=6)

class DuressSetupForm(forms.Form):
    decoy_password = forms.CharField(label="Duress/Decoy Password", required=True)

class RecoveryKeyConfirmForm(forms.Form):
    recovery_key = forms.CharField(label="Recovery Key", required=True, max_length=255)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
