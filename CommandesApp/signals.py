from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Commande
from LivraisonApp.models import Livraison

@receiver(post_save, sender=Commande)
def update_livraison_address(sender, instance, **kwargs):
    """
    Update all related Livraison objects whenever the Commande's
    adresse_livraison changes.
    """
    if instance.type_commande == "livraison":
        Livraison.objects.filter(commande=instance).update(adresse_livraison=instance.adresse_livraison)