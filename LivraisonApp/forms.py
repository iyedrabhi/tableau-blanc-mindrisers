from django import forms
from .models import Livraison


class LivraisonForm(forms.ModelForm):
    class Meta:
        model = Livraison

        # 🔹 Champs que le client manipule directement
        fields = [
            "id_commande",
            "adresse_complete",
            "latitude",
            "longitude",
        ]

        labels = {
            "id_commande": "Numéro de commande",
            "adresse_complete": "Adresse de livraison",
            "latitude": "Latitude",
            "longitude": "Longitude",
        }

        widgets = {
            "id_commande": forms.NumberInput(attrs={
                "placeholder": "Ex : 1023",
                "class": "form-control",
            }),
            "adresse_complete": forms.TextInput(attrs={
                "placeholder": "Ex : Rue Taieb El Mhiri, Monastir",
                "class": "form-control",
            }),
            # Ces deux champs seront remplis par la carte (JS),
            # on peut les afficher en readonly ou les cacher dans le template
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
        }
