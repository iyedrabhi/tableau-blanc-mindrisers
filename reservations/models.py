from django.db import models
from django.conf import settings  # pour le CustomUser
from tables.models import Table

class Reservation(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # Durée anticipée (en minutes) - utile pour le timer/prolongation métier
    duration_minutes = models.PositiveIntegerField(default=90, help_text='Durée anticipée en minutes')
    status = models.CharField(
        max_length=20,
        choices=[
            ('reserved', 'Réservé'),
            ('cancelled', 'Annulé'),
            ('finished', 'Terminé'),
        ],
        default='reserved'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # Rappel et suivi
    reminder_datetime = models.DateTimeField(blank=True, null=True, help_text='Moment où le rappel client doit être envoyé')
    reminder_sent = models.BooleanField(default=False)
    # Celery task id for the scheduled release task (to allow revocation)
    release_task_id = models.CharField(max_length=255, blank=True, null=True, help_text='Celery task id for scheduled release')

    def __str__(self):
        return f"Reservation {self.client.username} - Table {self.table.number} on {self.date} at {self.start_time}"


class Notification(models.Model):
    """Notifications en‑app / log d'envoi pour clients et gérant."""
    recipient_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    # type: 'manager' or 'client' (libre)
    notification_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Notification to {self.recipient_user} - {self.title[:30]}"
