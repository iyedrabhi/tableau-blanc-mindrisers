from celery import shared_task
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta

from .models import Reservation
from .services.notifications import create_inapp_notification, send_email_notification


@shared_task
def dispatch_due_reminders():
    """Periodic task run by beat: find reservations with reminder_datetime due and not sent."""
    now = timezone.now()
    # small window to catch reminders scheduled slightly in the past
    window_start = now - timedelta(minutes=1)
    window_end = now + timedelta(minutes=1)

    due = Reservation.objects.filter(
        date=now.date(),
        reminder_sent=False,
        reminder_datetime__gte=window_start,
        reminder_datetime__lte=window_end,
        status='reserved'
    )

    for r in due:
        send_reminder.delay(r.id)


@shared_task
def send_reminder(reservation_id):
    """Send smart reminder notification to client.
    
    Rules:
    - If reservation time < 12:00 (morning): send reminder 2 hours before
    - If reservation time >= 12:00 (afternoon/evening): send reminder 4 hours before
    """
    try:
        r = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return False

    user = r.client
    title = "Rappel : votre réservation aujourd'hui"
    
    # Smart reminder message based on reservation time
    if r.start_time.hour < 12:
        # Morning reservation (before 12:00): 2h before
        reminder_lead = "2 heures"
    else:
        # Afternoon/evening reservation (12:00 or later): 4h before
        reminder_lead = "4 heures"
    
    message = f"Rappel : Vous avez une réservation aujourd'hui à {r.start_time.strftime('%H:%M')} pour la Table {r.table.number}.\nMerci de vous présenter à temps."

    # Create in-app notification (use standardized 'RAPPEL')
    create_inapp_notification(user, title, message, notification_type='RAPPEL')

    # Try to send email according to user preferences
    try:
        pref = user.notification_pref
    except Exception:
        pref = None

    if pref is None or pref.email_reminders:
        if user.email:
            send_email_notification(user.email, title, message)

    r.reminder_sent = True
    r.save(update_fields=['reminder_sent'])
    return True


@shared_task
def start_reservation_timer(reservation_id):
    """Schedule a release task for the reservation based on its expected duration."""
    try:
        r = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return False

    # compute end datetime: reservation.start_time + duration
    start_dt = datetime.combine(r.date, r.start_time)
    # ensure timezone-aware
    if timezone.is_naive(start_dt):
        start_dt = timezone.make_aware(start_dt)

    # duration in minutes
    end_dt = start_dt + timedelta(minutes=r.duration_minutes)

    # schedule release task to run end_dt + grace period (3 minutes)
    release_eta = end_dt + timedelta(minutes=3)
    result = release_table.apply_async(args=[r.id], eta=release_eta)

    # store task id on reservation for possible revocation
    try:
        r.release_task_id = result.id
        r.save(update_fields=['release_task_id'])
    except Exception:
        pass

    # Also schedule 20-min-before notification for client (if within future)
    notify_before = release_eta - timedelta(minutes=r.duration_minutes + 20)
    # Simpler: schedule a 20-min before end reminder via send_reminder? We'll rely on the reminder mechanism for pre-arrival.
    return True


@shared_task
def extend_reservation(reservation_id, extra_minutes):
    try:
        r = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return False

    r.duration_minutes = r.duration_minutes + int(extra_minutes)
    r.save(update_fields=['duration_minutes'])

    # Re-schedule release: revoke previous release task (if exists) then start a new timer
    try:
        from restaurant_project.celery import app as celery_app
        if r.release_task_id:
            celery_app.control.revoke(r.release_task_id, terminate=False)
    except Exception:
        pass

    start_reservation_timer.delay(r.id)

    # Notify managers about the prolongation
    staff_users = r.client.__class__.objects.filter(is_staff=True)
    title = f"Prolongation: Table {r.table.number} par {r.client.username}"
    message = f"La réservation {r.id} a été prolongée de {extra_minutes} minutes."
    for s in staff_users:
        # Use a clear staff-facing notification type
        create_inapp_notification(s, title, message, notification_type='PROLONGATION')
        if s.email:
            send_email_notification(s.email, title, message)

    return True


@shared_task
def release_table(reservation_id):
    try:
        r = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return False

    # Only release if still reserved
    if r.status == 'reserved':
        r.status = 'finished'
        r.release_task_id = None
        r.save(update_fields=['status', 'release_task_id'])

        # update the table synthetic flag (if used)
        t = r.table
        t.is_reserved = False
        t.save(update_fields=['is_reserved'])

        # Notify managers
        staff_users = r.client.__class__.objects.filter(is_staff=True)
        title = f"Table {t.number} libérée automatiquement"
        message = f"La table {t.number} réservée initialement par {r.client} le {r.date} a été libérée automatiquement."
        for s in staff_users:
            # Notify staff that the table was released
            create_inapp_notification(s, title, message, notification_type='RELEASE')
            if s.email:
                send_email_notification(s.email, title, message)

    return True
