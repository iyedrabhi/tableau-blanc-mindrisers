"""
Management command to test smart reminders WITHOUT Celery.
Creates a test reservation and sends the reminder after a countdown.
This simulates waiting for the scheduled reminder time.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta, time
import time as time_module
from reservations.models import Reservation, Notification
from tables.models import Table

User = get_user_model()


class Command(BaseCommand):
    help = "Test smart reminders WITHOUT Celery (simulates waiting for reminder time)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--wait',
            type=int,
            default=0,
            help='Seconds to wait before sending reminder (default: 0 = immediate)',
        )
        parser.add_argument(
            '--future',
            action='store_true',
            help='Create reminder for future time (tomorrow morning)',
        )

    def handle(self, *args, **options):
        wait_seconds = options.get('wait', 0)
        create_future = options.get('future', False)

        # Get test_client
        try:
            client = User.objects.get(username='test_client')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ test_client not found. Run setup_test_users first."))
            return

        # Get an available table
        try:
            table = Table.objects.first()
            if not table:
                self.stdout.write(self.style.ERROR("❌ No tables found in database."))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error getting table: {e}"))
            return

        # Get current time
        now = timezone.now()
        current_hour = now.hour

        self.stdout.write(f"\n⏰ Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

        # Create a test reservation
        today = now.date()

        if create_future or current_hour >= 12:
            # Future: Tomorrow morning 9:00 with 2h reminder
            today = today + timedelta(days=1)
            start_time = time(9, 0)
            end_time = time(10, 0)
            reminder_hours_before = 2
            time_category = "TOMORROW MORNING (2h reminder)"
        else:
            # Today afternoon 14:00 with 4h reminder
            start_time = time(14, 0)
            end_time = time(15, 0)
            reminder_hours_before = 4
            time_category = "TODAY AFTERNOON (4h reminder)"

        # Calculate reminder datetime
        reservation_datetime = timezone.make_aware(
            datetime.combine(today, start_time)
        )
        reminder_dt = reservation_datetime - timedelta(hours=reminder_hours_before)

        try:
            reservation = Reservation.objects.create(
                client=client,
                table=table,
                date=today,
                start_time=start_time,
                end_time=end_time,
                duration_minutes=60,
                reminder_datetime=reminder_dt,
                reminder_sent=False,
            )
            self.stdout.write(
                self.style.SUCCESS(f"\n✓ Test reservation created!")
            )
            self.stdout.write(f"\n📋 Reservation Details:")
            self.stdout.write(f"  • Client: {client.username}")
            self.stdout.write(f"  • Table: {table.number}")
            self.stdout.write(f"  • Date: {today.strftime('%Y-%m-%d')}")
            self.stdout.write(f"  • Time: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}")
            self.stdout.write(f"  • Category: {time_category}")
            self.stdout.write(f"\n⏰ Reminder Schedule:")
            self.stdout.write(f"  • Scheduled for: {reminder_dt.strftime('%Y-%m-%d %H:%M:%S')}")
            self.stdout.write(f"  • Time until reminder: {(reminder_dt - now).total_seconds() / 60:.1f} minutes")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error creating reservation: {e}"))
            return

        # Option: Wait before sending reminder
        if wait_seconds > 0:
            self.stdout.write(f"\n⏳ Waiting {wait_seconds} seconds before sending reminder...")
            for i in range(wait_seconds, 0, -1):
                self.stdout.write(f"  {i}s remaining...", ending='\r')
                time_module.sleep(1)
            self.stdout.write("  Sending now!        ")

        # Send the reminder manually (simulating what Celery beat would do)
        self.stdout.write("\n" + self.style.SUCCESS("🔔 Sending reminder..."))
        try:
            # Create notification for reminder
            notification = Notification.objects.create(
                recipient_user=client,
                title=f"⏰ Rappel de votre réservation",
                message=f"Rappel pour votre réservation à la Table {table.number} le {today.strftime('%d/%m/%Y')} à {start_time.strftime('%H:%M')}",
                notification_type='RAPPEL',
                read=False,
            )
            
            # Mark reminder as sent
            reservation.reminder_sent = True
            reservation.save()
            
            self.stdout.write(self.style.SUCCESS(f"✓ Reminder sent!"))
            self.stdout.write(f"  Notification ID: {notification.id}")
            self.stdout.write(f"  Message: {notification.message}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error sending reminder: {e}"))
            return

        # Instructions
        self.stdout.write("\n" + self.style.SUCCESS("✅ Test complete!"))
        self.stdout.write(f"\n🔍 How to verify:")
        self.stdout.write(f"  1. Login as: test_client / Test@123")
        self.stdout.write(f"  2. Go to: http://127.0.0.1:8000/reservations/reminders/")
        self.stdout.write(f"  3. You should see the reminder notification")
        self.stdout.write(f"\n💡 Usage:")
        self.stdout.write(f"  • Without wait: python manage.py test_reminders_scheduled")
        self.stdout.write(f"  • With 5sec wait: python manage.py test_reminders_scheduled --wait 5")
        self.stdout.write(f"  • For tomorrow: python manage.py test_reminders_scheduled --future")


