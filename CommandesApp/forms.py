from .models import Commande , Plate
from django import forms


class CommandeForm(forms.ModelForm):
    plates = forms.ModelMultipleChoiceField(
        queryset=Plate.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Commande
        fields = ["plates", "type_commande", "comment","adresse_livraison"]
        widgets = {
            'adresse_livraison': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
