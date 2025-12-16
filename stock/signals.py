from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Crée automatiquement un profil lié à l'utilisateur
        UserProfile.objects.create(user=instance)
    else:
        # Vérifie que l'utilisateur a bien un profil avant de le sauvegarder
        try:
            instance.userprofile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)

