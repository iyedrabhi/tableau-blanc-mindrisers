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
        "commande",
        "customer",
        "adresse_livraison",
    )
    
    list_filter = ("statut",)  # Filtres à droite
    search_fields = ("id", "adresse_livraison")  # Barre de recherche
