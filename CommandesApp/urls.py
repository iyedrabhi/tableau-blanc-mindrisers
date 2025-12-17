from django.urls import path
from .views import *

urlpatterns = [
    path('create_commandes/', CommandeCreate.as_view(), name='commande_create'),
    path('', CommandeListView.as_view(), name='commande_list'),
    path('commandes_detail/<int:pk>/', CommandeDetailView.as_view(), name='commande_detail'),
    path('commandes_update/<int:pk>/', CommandeUpdateView.as_view(), name='commande_update'),
    path('commandes_delete/<int:pk>/', CommandeDeleteView.as_view(), name='commande_delete'),
    path("admin/commande/<int:pk>/", CommandeDetailAdminView.as_view(), name="commande_detail_admin"),
]
