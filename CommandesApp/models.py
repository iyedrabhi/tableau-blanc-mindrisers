from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import qrcode
from io import BytesIO
from django.core.files import File

class Plate(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="plates/", blank=True, null=True)

    def __str__(self):
        return self.title


class Commande(models.Model):
    STATUS_CHOICES = [
        ("En attente", "En attente"),
        ("En préparation", "En préparation"),
        ("Prête", "Prête"),
        ("Livrée", "Livrée"),
        ("Annulée", "Annulée"),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    plates = models.ManyToManyField('Plate', related_name='commandes')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    type_commande = models.CharField(
        max_length=20,
        choices=[("livraison", "Livraison"), ("sur place", "Sur place")]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="En attente")
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    def calculate_total_price(self):
        return sum(plate.price for plate in self.plates.all())

    def save(self, *args, **kwargs):
        # Sauvegarde initiale pour obtenir un PK si nécessaire
        super().save(*args, **kwargs)

    # Calculate total price
        new_total = self.calculate_total_price()
        if self.total_price != new_total:
            self.total_price = new_total

        # Generate QR code **in-memory**
        qr_data = f"Commande {self.id} - Client: {self.customer.username} - Statut: {self.status}"
        qr_img = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")

        # Use a fixed filename for this order
        filename = f"cmd_{self.id}.png"  # filename does NOT change

        # Replace old QR code file with the updated one
        self.qr_code.save(filename, File(buffer), save=False)

        # Save once at the end
        super().save(update_fields=["total_price", "qr_code"])


        # 🔥 AUTO CREATE LIVRAISON
        if self.type_commande == "livraison":
            from LivraisonApp.models import Livraison  # 👈 lazy import

            Livraison.objects.get_or_create(
                commande=self,
                defaults={"statut": "en_attente"}
            )

    def __str__(self):
        return f"Commande {self.id} - {self.customer.username}"



class Menu(models.Model):
    title = models.CharField(max_length=100)
    plates = models.ManyToManyField(Plate, related_name="menus")

    def __str__(self):
        return self.title
