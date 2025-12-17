from django.db import models
from django.utils import timezone
class Livraison(models.Model):

    STATUT_LIVRAISON = [
        ('en_cours', 'En cours'),
        ('prete', 'Prête'),
        ('en_attente', 'En attente'),
        ('livree', 'Livrée'),
        ('retour', 'Retour'),      # 🔥 nouveau statut

        ('annulee', 'Annulée'),

    ]

    date_sortie = models.DateTimeField(default=timezone.now)
    date_arrivee = models.DateTimeField(null=True, blank=True)
    commande = models.ForeignKey("CommandesApp.Commande", on_delete=models.CASCADE, related_name='livraison', null=True, blank=True)
    statut = models.CharField(
        max_length=20,
        choices=STATUT_LIVRAISON,
        default='en_cours'
    )

    id_livreur = models.IntegerField(null=True, blank=True)
    id_client = models.IntegerField(null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    adresse_complete = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Livraison commande #{self.Commande.id} - {self.statut}"
