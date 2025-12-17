from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta, time

from .models import Reservation
from .services.notifications import send_email_notification, create_inapp_notification
from .tasks import start_reservation_timer
from restaurant_project.celery import app as celery_app


@receiver(post_save, sender=Reservation)
def reservation_post_save(sender, instance: Reservation, created, **kwargs):
    # Lors de la création d'une réservation : calculer le rappel et notifier le gérant
    User = get_user_model()
    staff_users = User.objects.filter(is_staff=True)

    if created and instance.status == 'reserved':
        # calculer datetime du rappel selon règle fournie
        # si heure < 12h -> -2h, sinon -4h
        dt = datetime.combine(instance.date, instance.start_time)
        # timezone naive -> make aware using timezone.get_current_timezone
        if dt.hour < 12:
            reminder_dt = dt - timedelta(hours=2)
        else:
            reminder_dt = dt - timedelta(hours=4)

        # convert to aware in current timezone
        try:
            reminder_dt = timezone.make_aware(reminder_dt)
        except Exception:
            # already aware or timezone not configured
            pass

        instance.reminder_datetime = reminder_dt
        instance.save(update_fields=['reminder_datetime'])

        # Schedule reservation timer/release via Celery
        try:
            start_reservation_timer.delay(instance.id)
        except Exception:
            # If Celery not available during development, ignore
            pass

        # Notifier le(s) gérant(s)
        title = f"✅ Table {instance.table.number} réservée le {instance.date} à {instance.start_time}"
        message = f"La table {instance.table.number} a été réservée pour {instance.client} le {instance.date} à {instance.start_time}."
        for staff in staff_users:
            create_inapp_notification(staff, title, message, notification_type='CONFIRMATION')
            # attempt email
            if staff.email:
                send_email_notification(staff.email, title, message)

    # Si annulation : notifier les gérants
    if not created and instance.status == 'cancelled':
        title = f"❌ Annulation: Table {instance.table.number} le {instance.date} à {instance.start_time}"
        message = f"La réservation de la table {instance.table.number} du {instance.date} à {instance.start_time} a été annulée par {instance.client}."
        for staff in staff_users:
            create_inapp_notification(staff, title, message, notification_type='ANNULATION')
            if staff.email:
                send_email_notification(staff.email, title, message)
        # Revoke any scheduled release task
        try:
            if instance.release_task_id:
                celery_app.control.revoke(instance.release_task_id, terminate=False)
                instance.release_task_id = None
                instance.save(update_fields=['release_task_id'])
        except Exception:
            pass
