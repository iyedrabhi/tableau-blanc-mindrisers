from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create test client and gerant users (idempotent)'

    def handle(self, *args, **options):
        User = get_user_model()

        if not User.objects.filter(username='test_client').exists():
            User.objects.create_user('test_client', 'client@example.com', 'clientpass')
            self.stdout.write(self.style.SUCCESS('Created user: test_client / clientpass'))
        else:
            self.stdout.write('User test_client already exists')

        if not User.objects.filter(username='test_gerant').exists():
            u = User.objects.create_user('test_gerant', 'gerant@example.com', 'gerantpass')
            u.is_staff = True
            u.save()
            self.stdout.write(self.style.SUCCESS('Created user: test_gerant / gerantpass (is_staff=True)'))
        else:
            self.stdout.write('User test_gerant already exists')

        self.stdout.write('Done')
