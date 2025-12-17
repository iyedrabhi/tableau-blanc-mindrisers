#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Dictionnaire: username -> password
passwords = {
    'gerant': 'gerant123',
    'meriem': 'meriem123',
    'admin': 'admin123',
    'client1': 'client123',
    'client2': 'client123',
    'gerant1': 'gerant123',
}

print("=" * 80)
print("RÉINITIALISATION DES PASSWORDS")
print("=" * 80)

for username, password in passwords.items():
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✅ {username:<20} → Password: {password}")
    except User.DoesNotExist:
        print(f"❌ {username:<20} → Utilisateur non trouvé")

print("=" * 80)
print("✅ Tous les passwords ont été réinitialisés !")
print("=" * 80)
