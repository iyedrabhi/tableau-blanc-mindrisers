from django import forms
from .models import Livraison
from django.contrib.auth.models import User

STATUT_CHOICES = [
    ("En cours de livraison", "En cours de livraison"),
    ("Prête", "Prête"),
    ("Livrée", "Livrée"),
    ("Annulée", "Annulée"),
]

class LivraisonForm(forms.ModelForm):
    statut = forms.ChoiceField(choices=STATUT_CHOICES)
    id_livreur = forms.ModelChoiceField(
        queryset=User.objects.all(),  # tous les users, pas de filtre
        required=False,
        empty_label="Non affecté"
    )

    class Meta:
        model = Livraison
        fields = ['customer', 'commande', 'adresse_livraison', 'statut', 'id_livreur']
        widgets = {
            'customer': forms.TextInput(attrs={'readonly': 'readonly'}),
            'commande': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

        # formulaire pour que le client saisisse son ID
class ClientLivraisonSearchForm(forms.Form):
    customer = forms.IntegerField(label="customer", required=True)


""" from django import forms
from .models import Livraison
from django.contrib.auth import get_user_model

User = get_user_model()

STATUT_CHOICES = [
    ("Prête", "Prête"),
    ("Livrée", "Livrée"),
    ("Annulée", "Annulée"),
]

class LivraisonForm(forms.ModelForm):
    id_livreur = forms.ModelChoiceField(
        queryset=User.objects.filter(role='livreur'),  # filtre par role
        required=False,
        label="Livreur",
        empty_label="Sélectionner un livreur"
    )

    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        label="Statut"
    )

    class Meta:
        model = Livraison
        fields = ['customer', 'commande', 'adresse_livraison', 'statut', 'id_livreur']
        widgets = {
            'customer': forms.TextInput(attrs={'readonly': 'readonly'}),
            'commande': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
"""