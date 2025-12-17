from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class Livraison(models.Model):

    STATUT_LIVRAISON = [
        ("En attente", "En attente"),
        ("En préparation", "En préparation"),
        ("Prête", "Prête"),
        ("En cours de livraison", "En cours de livraison"),

        ("Livrée", "Livrée"),
        ("Annulée", "Annulée"),
    ]


    date_sortie = models.DateTimeField(default=timezone.now)
    date_arrivee = models.DateTimeField(null=True, blank=True)
    commande = models.ForeignKey("CommandesApp.Commande", on_delete=models.CASCADE, related_name='livraison', null=True, blank=True)
    statut = models.CharField(
        max_length=30,
        choices=STATUT_LIVRAISON,
        default='en_cours'
    )

    id_livreur = models.IntegerField(null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='livraisons')
    adresse_livraison = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Livraison commande #{self.commande.id if self.commande else 'N/A'} - {self.statut}"
    # In Livraison model
    @property
    def maps_link(self):
        if self.adresse_livraison:
            import urllib.parse
            addr = urllib.parse.quote_plus(self.adresse_livraison)
            return f"https://www.google.com/maps/search/?api=1&query={addr}"
        return None

    def save(self, *args, **kwargs):
    # Récupérer l'adresse de la commande si non définie
        if not self.adresse_livraison and self.commande:
            self.adresse_livraison = self.commande.adresse_livraison

        # Si livraison Livrée et date_arrivee vide
        if self.statut == "Livrée" and not self.date_arrivee:
            self.date_arrivee = timezone.now()

        # Vérifier si instance déjà existante (update) pour synchroniser la commande
        is_update = self.pk is not None

        super().save(*args, **kwargs)

        # 🔄 Synchroniser le statut de la commande uniquement si update ET type_commande == 'livraison'
        if is_update and self.commande and self.commande.type_commande == "livraison":
            if self.commande.status != self.statut:
                self.commande.status = self.statut
                self.commande.save(update_fields=['status'])

