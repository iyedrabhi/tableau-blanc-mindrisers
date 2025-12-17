from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

from reservations.models import Reservation
from reservations.services.notifications import send_email_notification, create_inapp_notification


class Command(BaseCommand):
    help = 'Envoie les rappels clients pour les réservations du jour selon la règle intelligente'

    def handle(self, *args, **options):
        now = timezone.now()
        today = now.date()

        # Rappels programmés pour aujourd'hui non envoyés et reminder_datetime dans le passé (ou proche)
        window_start = now - timedelta(minutes=1)
        window_end = now + timedelta(minutes=5)

        reservations = Reservation.objects.filter(
            date=today,
            reminder_sent=False,
            reminder_datetime__gte=window_start,
            reminder_datetime__lte=window_end,
            status='reserved',
        )

        self.stdout.write(f'Found {reservations.count()} reminders to send')

        for r in reservations:
            user = r.client
            title = 'Rappel : votre réservation aujourd\'hui'
            message = f"Rappel : Vous avez une réservation aujourd'hui à {r.start_time} pour la Table {r.table.number}."

            # create in-app
            create_inapp_notification(user, title, message, notification_type='client')

            # optionally send email if user pref allows
            try:
                pref = user.notification_pref
            except Exception:
                pref = None

            if pref is None or pref.email_reminders:
                if user.email:
                    send_email_notification(user.email, title, message)

            # mark sent
            r.reminder_sent = True
            r.save(update_fields=['reminder_sent'])

            self.stdout.write(f'Sent reminder for reservation {r.id} to {user}')
