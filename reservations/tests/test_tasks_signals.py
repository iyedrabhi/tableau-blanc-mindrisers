from django.test import TestCase
from django.utils import timezone
from datetime import date, time, timedelta
from unittest.mock import patch, MagicMock, call
from asgiref.sync import async_to_sync

from reservations.models import Reservation, Notification
from tables.models import Table
from client.models import CustomUser

class TasksSignalsTests(TestCase):
    def setUp(self):
        # Create a client user and a staff user
        self.client_user = CustomUser.objects.create_user(username='u1', email='u1@example.com', password='pass')
        self.staff_user = CustomUser.objects.create_user(username='manager', email='m@example.com', password='pass', is_staff=True)
        # table
        self.table = Table.objects.create(number=1, seats=4)

    @patch('reservations.tasks.release_table.apply_async')
    def test_start_reservation_timer_saves_task_id(self, mock_apply_async):
        # mock apply_async returning object with id
        mock_result = MagicMock()
        mock_result.id = 'task-123'
        mock_apply_async.return_value = mock_result

        r = Reservation.objects.create(
            client=self.client_user,
            table=self.table,
            date=date.today(),
            start_time=time(12,0),
            end_time=time(13,30),
            duration_minutes=90
        )

        # call the task function directly
        from reservations.tasks import start_reservation_timer
        start_reservation_timer(r.id)

        r.refresh_from_db()
        self.assertEqual(r.release_task_id, 'task-123')

    @patch('reservations.tasks.start_reservation_timer.delay')
    def test_signal_on_create_sets_reminder_and_schedules_timer(self, mock_start_delay):
        # create reservation - the post_save signal should run
        r = Reservation.objects.create(
            client=self.client_user,
            table=self.table,
            date=date.today(),
            start_time=time(18,0),
            end_time=time(19,30),
        )
        r.refresh_from_db()
        # reminder_datetime should be set according to rules (hour>=12 -> -4h)
        self.assertIsNotNone(r.reminder_datetime)
        # ensure start_reservation_timer.delay was called
        mock_start_delay.assert_called_with(r.id)

    @patch('restaurant_project.celery.app.control.revoke')
    def test_cancel_revoke_release_task(self, mock_revoke):
        r = Reservation.objects.create(
            client=self.client_user,
            table=self.table,
            date=date.today(),
            start_time=time(12,0),
            end_time=time(13,30),
            duration_minutes=90
        )
        # set a fake release_task_id and save
        r.release_task_id = 't-999'
        r.save(update_fields=['release_task_id'])

        # simulate cancellation: change status and call the signal manually
        from reservations.signals import reservation_post_save
        r.status = 'cancelled'
        reservation_post_save(sender=Reservation, instance=r, created=False)

        r.refresh_from_db()
        self.assertIsNone(r.release_task_id)
        mock_revoke.assert_called()


class NotificationChannelTests(TestCase):
    def setUp(self):
        self.client_user = CustomUser.objects.create_user(username='u1', email='u1@example.com', password='pass')
        self.staff_user = CustomUser.objects.create_user(username='manager', email='m@example.com', password='pass', is_staff=True)

    @patch('reservations.services.notifications.get_channel_layer')
    def test_create_inapp_notification_creates_db_record(self, mock_get_channel_layer):
        # mock channel layer
        mock_channel_layer = MagicMock()
        mock_get_channel_layer.return_value = mock_channel_layer

        from reservations.services.notifications import create_inapp_notification

        title = 'Test Notification'
        message = 'This is a test message'
        create_inapp_notification(self.client_user, title, message, notification_type='client')

        # verify DB notification created
        notif = Notification.objects.get(recipient_user=self.client_user)
        self.assertEqual(notif.title, title)
        self.assertEqual(notif.message, message)
        self.assertEqual(notif.notification_type, 'client')

    @patch('reservations.services.notifications.get_channel_layer')
    @patch('reservations.services.notifications.async_to_sync')
    def test_create_inapp_notification_sends_to_user_group(self, mock_async_to_sync, mock_get_channel_layer):
        # Setup mocks
        mock_channel_layer = MagicMock()
        mock_get_channel_layer.return_value = mock_channel_layer
        mock_group_send = MagicMock()
        mock_channel_layer.group_send = mock_group_send
        mock_async_to_sync.side_effect = lambda func: func  # identity wrapper for testing

        from reservations.services.notifications import create_inapp_notification

        title = 'Test Notification'
        message = 'Test message'
        create_inapp_notification(self.client_user, title, message, notification_type='client')

        # verify group_send was called with correct user group
        expected_group_name = f'user_{self.client_user.id}'
        mock_group_send.assert_called()

    @patch('reservations.services.notifications.get_channel_layer')
    @patch('reservations.services.notifications.async_to_sync')
    def test_create_inapp_notification_sends_to_managers_group_when_type_manager(self, mock_async_to_sync, mock_get_channel_layer):
        # Setup mocks
        mock_channel_layer = MagicMock()
        mock_get_channel_layer.return_value = mock_channel_layer
        mock_group_send = MagicMock()
        mock_channel_layer.group_send = mock_group_send
        mock_async_to_sync.side_effect = lambda func: func  # identity wrapper for testing

        from reservations.services.notifications import create_inapp_notification

        title = 'Manager Notification'
        message = 'This is for managers'
        create_inapp_notification(self.staff_user, title, message, notification_type='manager')

        # verify group_send was called with 'managers' group
        mock_group_send.assert_called()

    @patch('reservations.services.notifications.get_channel_layer')
    def test_create_inapp_notification_handles_missing_channel_layer(self, mock_get_channel_layer):
        # simulate missing channel layer
        mock_get_channel_layer.side_effect = Exception('Channel layer not configured')

        from reservations.services.notifications import create_inapp_notification

        # should not raise, but create the DB notification
        notif = create_inapp_notification(self.client_user, 'Test', 'Message', notification_type='client')
        self.assertIsNotNone(notif.id)
        self.assertEqual(notif.recipient_user, self.client_user)
