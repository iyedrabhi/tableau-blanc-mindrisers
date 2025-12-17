#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Créer ou mettre à jour l'admin
user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@test.com',
        'is_staff': True,
        'is_superuser': True
    }
)

if created:
    user.set_password('admin123')
    user.save()
    print("✅ Admin 'admin' créé avec succès !")
    print("📝 Username: admin")
    print("🔑 Password: admin123")
else:
    print("✅ Admin existe déjà")
    # Mettre à jour le mot de passe juste au cas où
    user.set_password('admin123')
    user.save()
    print("🔑 Password mis à jour: admin123")
