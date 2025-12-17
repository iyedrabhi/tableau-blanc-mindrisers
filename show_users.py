#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
users = User.objects.all()

print("=" * 80)
print(f"{'Username':<20} {'Email':<30} {'Staff':<8} {'Superuser':<12}")
print("=" * 80)

if users.count() == 0:
    print("❌ Aucun utilisateur trouvé!")
else:
    for u in users:
        staff = "✅" if u.is_staff else "❌"
        superuser = "✅" if u.is_superuser else "❌"
        print(f"{u.username:<20} {u.email:<30} {staff:<8} {superuser:<12}")

print("=" * 80)
print(f"Total: {users.count()} utilisateur(s)")
print("=" * 80)
