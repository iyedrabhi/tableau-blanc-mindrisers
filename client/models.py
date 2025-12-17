from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    """
    Modèle utilisateur étendu pour le système de réservation.
    Prépare le terrain pour IA future et fonctionnalités clients.
    """

    # Informations personnelles de base
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    # Préférences de réservation (préparation IA)
    preferred_zone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Zone préférée pour la table : terrasse, intérieur, etc."
    )
    prefers_vip = models.BooleanField(
        default=False,
        help_text="Indique si le client préfère une table VIP"
    )

    # Historique / scoring pour IA future
    frequent_customer_score = models.FloatField(
        default=0.0,
        help_text="Score calculé selon le nombre et fréquence de réservations"
    )

    # Notes internes
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Remarques internes sur le client : allergies, préférences spécifiques..."
    )

    # Méthode string pour afficher le client facilement
    def __str__(self):
        return f"{self.username} ({self.email})"


class NotificationPreference(models.Model):
    """Préférences de notification par utilisateur."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_pref')
    email_reminders = models.BooleanField(default=True)
    sms_reminders = models.BooleanField(default=False)
    inapp_reminders = models.BooleanField(default=True)

    def __str__(self):
        return f"NotificationPreference({self.user.username})"
