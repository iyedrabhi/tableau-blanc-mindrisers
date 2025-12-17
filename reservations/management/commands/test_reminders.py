"""
Management command to test smart reminders by creating a test reservation
with a reminder time set to NOW (so it triggers immediately).
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta, time
from reservations.models import Reservation
from tables.models import Table
from reservations.tasks import send_reminder

User = get_user_model()


class Command(BaseCommand):
    help = "Test smart reminders by creating a test reservation"

    def handle(self, *args, **options):
        # Get test_client
        try:
            client = User.objects.get(username='test_client')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ test_client not found. Run setup_test_users first."))
            return

        # Get an available table (or create one)
        try:
            table = Table.objects.first()
            if not table:
                self.stdout.write(self.style.ERROR("❌ No tables found in database."))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error getting table: {e}"))
            return

        # Create a test reservation for TODAY at 14:00 (afternoon)
        today = timezone.now().date()
        start_time = time(14, 0)  # 14:00 (afternoon, so 4h before = 10:00)
        end_time = time(15, 0)
        
        # Calculate reminder: 4 hours before 14:00 = 10:00
        reminder_dt = timezone.make_aware(
            datetime.combine(today, start_time) - timedelta(hours=4)
        )

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
                self.style.SUCCESS(f"✓ Test reservation created: {reservation}")
            )
            self.stdout.write(f"  Table: {table.number}")
            self.stdout.write(f"  Date: {today}")
            self.stdout.write(f"  Time: {start_time} - {end_time}")
            self.stdout.write(f"  Reminder scheduled for: {reminder_dt}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error creating reservation: {e}"))
            return

        # Now manually trigger the reminder task
        self.stdout.write("\n" + self.style.SUCCESS("🔔 Triggering reminder manually..."))
        try:
            result = send_reminder(reservation.id)
            if result:
                self.stdout.write(self.style.SUCCESS(f"✓ Reminder sent! Check notifications page."))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Reminder task returned False"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error sending reminder: {e}"))
            return

        self.stdout.write("\n" + self.style.SUCCESS("✅ Test complete!"))
        self.stdout.write(f"Login as test_client / Test@123")
        self.stdout.write(f"Go to: http://127.0.0.1:8000/reservations/notifications/")
        self.stdout.write(f"You should see the reminder notification there.")
