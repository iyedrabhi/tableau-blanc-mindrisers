from django.contrib import admin
from .models import Livraison

@admin.register(Livraison)
class LivraisonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "statut",
        "date_sortie",
        "date_arrivee",
        "id_livreur",
        "id_commande",
        "id_client",
        "adresse_complete",
    )
    
    list_filter = ("statut",)  # Filtres à droite
    search_fields = ("id", "adresse_complete")  # Barre de recherche
