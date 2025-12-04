from django.urls import path
from . import views

urlpatterns = [
    path("livraisons/", views.livraison_list, name="livraison_list"),
    path("livraisons/client/", views.livraison_list_client, name="livraison_list_client"),
    path("livraisons/ajouter/", views.livraison_create, name="livraison_create"),
    path("livraisons/<int:pk>/modifier/", views.livraison_update, name="livraison_update"),
    path("livraisons/<int:pk>/supprimer/", views.livraison_delete, name="livraison_delete"),

    
  path(
        "livraisons/<int:pk>/update-row/",
        views.livraison_update_row,
        name="livraison_update_row",
    ),

    path("livraisons/<int:pk>/detail/", views.livraison_detail, name="livraison_detail"),
    path("livraisons/<int:pk>/annuler/", views.livraison_annuler, name="livraison_annuler"),
    path("livraisons/creer/", views.livraison_create_gerant, name="livraison_create_gerant"),
# Vue liste pour un livreur donné
path(
    "livreur/<int:livreur_id>/livraisons/",
    views.livreur_livraisons,
    name="livreur_livraisons",
),

# Mise à jour du statut d'une livraison par le livreur (inline dans le tableau)
path(
    "livreur/<int:livreur_id>/livraisons/<int:pk>/update/",
    views.livreur_update_statut_row,
    name="livreur_update_statut_row",
),

        # 🔽 ROUTES API POUR POSTMAN
    path("api/livraisons/", views.livraison_list_create_api, name="api_livraisons"),
    path("api/livraisons/<int:pk>/", views.livraison_detail_api, name="api_livraison_detail"),
]

