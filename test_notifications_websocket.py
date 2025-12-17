#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour creer une notification et verifier WebSocket
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from client.models import CustomUser
from reservations.models import Notification, Reservation
from reservations.services.notifications import create_inapp_notification
from tables.models import Table

print("="*70)
print("TEST NOTIFICATIONS - WEBSOCKET")
print("="*70)

# Recup utilisateur client
try:
    client = CustomUser.objects.get(username='client1')
    print(f"\n[OK] User found: {client.username}")
except CustomUser.DoesNotExist:
    print("\n[ERROR] Client user 'client1' not found!")
    exit(1)

# Recup utilisateur gerant
try:
    gerant = CustomUser.objects.get(username='gerant', is_staff=True)
    print(f"[OK] Manager found: {gerant.username}")
except CustomUser.DoesNotExist:
    print("[ERROR] Manager user 'gerant' not found!")
    gerant = None

print("\n" + "="*70)
print("TEST 1: CREATION NOTIFICATION CLIENT")
print("="*70)

title1 = "Test Notification Client"
message1 = "Ceci est une notification de test pour le client"

notif1 = create_inapp_notification(client, title1, message1, notification_type='client')
print(f"\n[OK] Notification creee:")
print(f"  - ID: {notif1.id}")
print(f"  - Titre: {notif1.title}")
print(f"  - Type: {notif1.notification_type}")
print(f"  - Utilisateur: {notif1.recipient_user.username}")

print("\n" + "="*70)
print("TEST 2: CREATION NOTIFICATION GERANT")
print("="*70)

if gerant:
    title2 = "Test Notification Manager"
    message2 = "Ceci est une notification de test pour le gerant"
    
    notif2 = create_inapp_notification(gerant, title2, message2, notification_type='manager')
    print(f"\n[OK] Notification creee pour le gerant:")
    print(f"  - ID: {notif2.id}")
    print(f"  - Type: {notif2.notification_type}")
    print(f"  - Utilisateur: {notif2.recipient_user.username}")

print("\n" + "="*70)
print("VERIFICATION BASE DE DONNEES")
print("="*70)

notifs = Notification.objects.all().order_by('-created_at')[:5]
print(f"\nDernieres notifications en base:")
for n in notifs:
    print(f"  [{n.id}] {n.notification_type:10} => {n.recipient_user.username:10}")

print("\n" + "="*70)
print("INSTRUCTIONS POUR TESTER")
print("="*70)
print("""
1. Assure-toi que le serveur tourne:
   source .../env_restaurant/Scripts/activate
   python manage.py runserver

2. Ouvre DEUX onglets du navigateur:
   - Onglet 1 (CLIENT): http://127.0.0.1:8000/reservations/available/
   - Onglet 2 (GERANT): http://127.0.0.1:8000/reservations/gerant/

3. Connecte-toi:
   - Onglet 1: client1 / client123
   - Onglet 2: gerant / gerant123

4. Tu devrais voir des toasts dans les deux onglets INDEPENDANTS!
   - Les deux connexions WebSocket sont SEPAREES
   - Chaque onglet a sa propre session
   - Les notifications arrivent en temps reel
""")

print("\n[OK] TEST COMPLETE")
print("="*70)
