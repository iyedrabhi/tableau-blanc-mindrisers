from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


# -------------------------
# Modèle StockItem
# -------------------------
class StockItem(models.Model):
    CATEGORY_CHOICES = [
        ("Viande", "Viande"),
        ("Légume", "Légume"),
        ("Fruit", "Fruit"),
        ("Épice", "Épice"),
        ("Boisson", "Boisson"),
        ("Autre", "Autre"),
    ]

    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    threshold = models.IntegerField()
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="Autre",
        db_index=True
    )
    expiration_date = models.DateField(null=True, blank=True)

    def is_low_stock(self):
        return self.quantity <= self.threshold

    def is_expired(self):
        if self.expiration_date:
            return self.expiration_date < timezone.now().date()
        return False

    def is_expiring_soon(self, days=7):
        if not self.expiration_date:
            return False
        today = timezone.now().date()
        return today <= self.expiration_date <= today + timedelta(days=days)

    def get_unit(self):
        """Retourne l’unité selon la catégorie"""
        if self.category in ["Légume", "Fruit", "Viande"]:
            return "kg"
        elif self.category == "Boisson":
            return "L"
        elif self.category == "Épice":
            return "g"
        else:
            return "u"  # unités

    def __str__(self):
        return self.name


# -------------------------
# Modèle UserProfile (rôle)
# -------------------------
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('chef', 'Chef'),
        ('staff', 'Staff'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='staff'
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ✅ Signal pour créer automatiquement un profil quand un User est créé
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# -------------------------
# Modèle OrderItem (commande)
# -------------------------
class OrderItem(models.Model):
    product = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def apply_stock(self):
        """Incrémente le stock quand une commande est validée (réception)"""
        # Augmente la quantité du produit par la quantité commandée
        self.product.quantity += self.quantity
        self.product.save()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


