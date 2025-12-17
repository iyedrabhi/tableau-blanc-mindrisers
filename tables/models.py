from django.db import models


class Table(models.Model):
    ZONE_CHOICES = [
        ('VIP', 'VIP'),
        ('Standard', 'Standard'),
        ('Terrasse', 'Terrasse'),
    ]

    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField()
    zone = models.CharField(max_length=50, choices=ZONE_CHOICES, blank=True, null=True)
    # Nouveau champs pour les métiers avancés
    category = models.CharField(max_length=50, blank=True, null=True, help_text='Catégorie: Standard, VIP, Famille...')
    location = models.CharField(max_length=50, blank=True, null=True, help_text='Emplacement: intérieur, terrasse...')
    ambiance = models.CharField(max_length=100, blank=True, null=True, help_text='Vue / ambiance')
    # Accessibilité
    pmr = models.BooleanField(default=False, help_text='Accessible aux personnes à mobilité réduite')
    highchair = models.BooleanField(default=False, help_text='Chaise haute disponible')
    power = models.BooleanField(default=False, help_text='Prise électrique disponible')
    wifi = models.BooleanField(default=False, help_text='Accès Wifi à proximité')
    special_status = models.CharField(max_length=100, blank=True, null=True, help_text='Statut spécial (ex: événement, VIP)')
    # Champ synthétique (peut rester pour compatibilité)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.number} - {self.zone or 'Non spécifié'}"
