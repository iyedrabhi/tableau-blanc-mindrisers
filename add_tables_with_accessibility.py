#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from tables.models import Table

# Supprimer les tables existantes (optionnel - décommenter si tu veux reset)
# Table.objects.all().delete()

tables_data = [
    # Tables Standard
    {
        'number': 1,
        'zone': 'Zone A',
        'capacity': 2,
        'category': 'Standard',
        'location': 'intérieur',
        'ambiance': 'Coin calme',
        'pmr': False,
        'highchair': False,
        'power': True,
        'wifi': True,
    },
    {
        'number': 2,
        'zone': 'Zone A',
        'capacity': 4,
        'category': 'Standard',
        'location': 'intérieur',
        'ambiance': 'Central',
        'pmr': False,
        'highchair': True,  # ← Chaise haute
        'power': True,
        'wifi': True,
    },
    {
        'number': 3,
        'zone': 'Zone A',
        'capacity': 6,
        'category': 'Standard',
        'location': 'intérieur',
        'ambiance': 'Lumineux',
        'pmr': True,  # ← PMR
        'highchair': False,
        'power': True,
        'wifi': True,
    },
    # Tables VIP
    {
        'number': 4,
        'zone': 'Zone B',
        'capacity': 4,
        'category': 'VIP',
        'location': 'intérieur',
        'ambiance': 'Privé, Vue sur jardin',
        'pmr': True,  # ← PMR
        'highchair': False,
        'power': True,
        'wifi': True,
    },
    {
        'number': 5,
        'zone': 'Zone B',
        'capacity': 2,
        'category': 'VIP',
        'location': 'terrasse',
        'ambiance': 'Romantique, Vue panoramique',
        'pmr': False,
        'highchair': False,
        'power': True,
        'wifi': True,
    },
    # Tables Famille
    {
        'number': 6,
        'zone': 'Zone C',
        'capacity': 8,
        'category': 'Famille',
        'location': 'intérieur',
        'ambiance': 'Spacieux, Jardin intérieur',
        'pmr': False,
        'highchair': True,  # ← Chaise haute
        'power': True,
        'wifi': True,
    },
    {
        'number': 7,
        'zone': 'Zone C',
        'capacity': 6,
        'category': 'Famille',
        'location': 'terrasse',
        'ambiance': 'Plein air, Aire de jeux proche',
        'pmr': True,  # ← PMR
        'highchair': True,  # ← Chaise haute
        'power': False,
        'wifi': True,
    },
    # Terrasse
    {
        'number': 8,
        'zone': 'Zone D',
        'capacity': 4,
        'category': 'Standard',
        'location': 'terrasse',
        'ambiance': 'Vue sur rue, Ensoleillée',
        'pmr': True,  # ← PMR
        'highchair': False,
        'power': False,
        'wifi': True,
    },
    {
        'number': 9,
        'zone': 'Zone D',
        'capacity': 3,
        'category': 'VIP',
        'location': 'terrasse',
        'ambiance': 'Isolée, Végétation',
        'pmr': False,
        'highchair': False,
        'power': True,
        'wifi': True,
    },
    # Table accessible avec tous les services
    {
        'number': 10,
        'zone': 'Zone E',
        'capacity': 5,
        'category': 'Famille',
        'location': 'intérieur',
        'ambiance': 'Accessible, Bien aéré',
        'pmr': True,  # ← PMR
        'highchair': True,  # ← Chaise haute
        'power': True,
        'wifi': True,
    },
]

print("=" * 80)
print("AJOUT DES TABLES AVEC ACCESSIBILITÉ")
print("=" * 80)

for data in tables_data:
    table, created = Table.objects.get_or_create(
        number=data['number'],
        defaults=data
    )
    if created:
        print(f"✅ Table {table.number:<3} → {table.category:<10} | {table.location:<10} | PMR: {table.pmr} | Chaise: {table.highchair}")
    else:
        print(f"⚠️  Table {table.number:<3} existe déjà (mise à jour ignorée)")

print("=" * 80)
print(f"✅ Total: {Table.objects.count()} tables en base de données")
print("=" * 80)
