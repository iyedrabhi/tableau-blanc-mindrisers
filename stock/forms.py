from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StockItem, UserProfile


# -------------------------
# Formulaire pour les stocks
# -------------------------
class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ["name", "quantity", "threshold", "category", "expiration_date"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "threshold": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),  # ✅ dropdown
            "expiration_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


# -------------------------
# Formulaire d'inscription utilisateur
# -------------------------
class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[("manager", "Manager"), ("chef", "Chef"), ("staff", "Staff")],
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "role")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=commit)  # crée l’utilisateur avec UserCreationForm
        if commit:
            # Associe un profil avec rôle
            UserProfile.objects.create(user=user, role=self.cleaned_data["role"])
        return user
