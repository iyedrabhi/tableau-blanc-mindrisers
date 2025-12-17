"""
Management command to set up test users for development.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Set up test users for development (client and gérant)"

    def handle(self, *args, **options):
        # Create or update test_client
        client, client_created = User.objects.get_or_create(
            username='test_client',
            defaults={
                'email': 'client@test.com',
                'is_staff': False,
                'is_active': True,
            }
        )
        client.set_password('Test@123')
        client.save()
        self.stdout.write(
            self.style.SUCCESS(f"✓ test_client: {'created' if client_created else 'updated'}")
            + f" | email={client.email} | is_staff={client.is_staff}"
        )

        # Create or update test_gerant
        gerant, gerant_created = User.objects.get_or_create(
            username='test_gerant',
            defaults={
                'email': 'gerant@test.com',
                'is_staff': True,
                'is_active': True,
            }
        )
        gerant.set_password('Gerant@123')
        gerant.save()
        self.stdout.write(
            self.style.SUCCESS(f"✓ test_gerant: {'created' if gerant_created else 'updated'}")
            + f" | email={gerant.email} | is_staff={gerant.is_staff}"
        )

        self.stdout.write("\n" + self.style.SUCCESS("✅ Test users are ready!"))
        self.stdout.write("  Client Login: test_client / Test@123")
        self.stdout.write("  Gérant Login: test_gerant / Gerant@123")
