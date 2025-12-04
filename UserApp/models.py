from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid

# utilities
def generate_userid():
	return "USER" + uuid.uuid4().hex[:4].upper()

name_validator = RegexValidator(regex=r'^[A-Za-z\s-]+$')


class User(AbstractUser):
	user_id = models.CharField(max_length=8, primary_key=True, unique=True, editable=False)
	first_name = models.CharField(max_length=50, validators=[name_validator])
	last_name = models.CharField(max_length=50, validators=[name_validator])
	email = models.EmailField(unique=True)
	# role differentiates between gerant, client and livreur
	ROLE = [
		("gerant", "Gérant"),
		("client", "Client"),
		("livreur", "Livreur"),
	]
	role = models.CharField(max_length=20, choices=ROLE, default="client")
	phone_number = models.CharField(max_length=20, blank=True, null=True)
	
	# Gérant fields
	restaurant_name = models.CharField(max_length=255, blank=True)
	restaurant_address = models.CharField(max_length=255, blank=True)
	restaurant_phone = models.CharField(max_length=20, blank=True)
	siret = models.CharField(max_length=50, blank=True, verbose_name="SIRET")
	business_license = models.CharField(max_length=100, blank=True)
	
	# Client fields
	living_location = models.CharField(max_length=255, blank=True)
	is_subscribed = models.BooleanField(default=False)
	date_of_birth = models.DateField(blank=True, null=True)
	
	# Livreur fields
	vehicle_number = models.CharField(max_length=50, blank=True)
	vehicle_type = models.CharField(
		max_length=50,
		choices=[("bike", "Bike"), ("scooter", "Scooter"), ("car", "Car"), ("motorcycle", "Motorcycle")],
		blank=True
	)
	vehicle_registration = models.CharField(max_length=100, blank=True)
	insurance_number = models.CharField(max_length=100, blank=True)
	is_available = models.BooleanField(default=True)
	bank_account = models.CharField(max_length=50, blank=True)

	# Soft delete flag to preserve records for export/history
	is_deleted = models.BooleanField(default=False)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		# Ensure superusers are always assigned the 'gerant' role
		if getattr(self, 'is_superuser', False):
			self.role = 'gerant'

		if not getattr(self, 'user_id', None):
			new_id = generate_userid()
			while User.objects.filter(user_id=new_id).exists():
				new_id = generate_userid()
			self.user_id = new_id
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.user_id} - {self.username}"


# Gérant: proxy model for restaurant managers
class Gerant(User):
	class Meta:
		proxy = True
		verbose_name = "Gérant"
		verbose_name_plural = "Gérants"


# Client: proxy model for customers
class Client(User):
	class Meta:
		proxy = True
		verbose_name = "Client"
		verbose_name_plural = "Clients"


# Livreur: proxy model for delivery drivers
class Livreur(User):
	class Meta:
		proxy = True
		verbose_name = "Livreur"
		verbose_name_plural = "Livreurs"
