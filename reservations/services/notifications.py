from django.core.mail import send_mail
from django.conf import settings
from ..models import Notification

# Channels
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_email_notification(to_email, subject, message):
    """Envoi simple d'email via la configuration Django EMAIL_*"""
    if not to_email:
        return False
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email], fail_silently=True)
    return True


def create_inapp_notification(user, title, message, notification_type=None):
    notif = Notification.objects.create(
        recipient_user=user,
        title=title,
        message=message,
        notification_type=notification_type
    )

    # Push real-time message via Channels
    try:
        channel_layer = get_channel_layer()
        payload = {
            'type': 'notification',
            'title': title,
            'message': message,
            'notification_type': notification_type,
        }
        # send to user personal group
        async_to_sync(channel_layer.group_send)(f'user_{user.id}', payload)

        # also send to managers group if the notification is for managers
        # support legacy 'manager' value plus standardized types
        # Broadcast to managers group for any staff-facing notification types.
        if notification_type in ('manager', 'CONFIRMATION', 'ANNULATION', 'PROLONGATION', 'RELEASE'):
            async_to_sync(channel_layer.group_send)('managers', payload)
    except Exception:
        # ignore if channel layer not configured
        pass

    return notif
