from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# ------------------------------
# General User Registration Form
# ------------------------------
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username", "first_name", "last_name", "email",
            "living_location", "date_of_birth",
            "password1", "password2",
        ]
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            "email": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            "living_location": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            "date_of_birth": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "password1": forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            "password2": forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
# ------------------------------
# Client Form
# ------------------------------
class ClientForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        required=False,
        help_text='Leave blank to keep the current password'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone_number',
            'living_location', 'date_of_birth', 'is_subscribed'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'living_location': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_subscribed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

# ------------------------------
# Livreur Form
# ------------------------------
class LivreurForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        required=False,
        help_text='Leave blank to keep the current password'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone_number',
            'vehicle_number', 'vehicle_type', 'vehicle_registration', 'is_available'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_registration': forms.TextInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
