#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from tables.models import Table

# DELETE ALL EXISTING TABLES
Table.objects.all().delete()
print('✅ All existing tables deleted')

tables_data = [
    # Tables Standard
    {
        'number': 1,
        'zone': 'Standard',
        'seats': 2,
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
        'zone': 'Standard',
        'seats': 4,
        'category': 'Standard',
        'location': 'intérieur',
        'ambiance': 'Central',
        'pmr': False,
        'highchair': True,
        'power': True,
        'wifi': True,
    },
    {
        'number': 3,
        'zone': 'Standard',
        'seats': 6,
        'category': 'Standard',
        'location': 'intérieur',
        'ambiance': 'Lumineux',
        'pmr': True,
        'highchair': False,
        'power': True,
        'wifi': True,
    },
    {
        'number': 4,
        'zone': 'Terrasse',
        'seats': 4,
        'category': 'Standard',
        'location': 'terrasse',
        'ambiance': 'Vue jardin',
        'pmr': False,
        'highchair': False,
        'power': True,
        'wifi': False,
    },
    # Tables VIP
    {
        'number': 5,
        'zone': 'VIP',
        'seats': 4,
        'category': 'VIP',
        'location': 'intérieur',
        'ambiance': 'Privé, Vue sur jardin',
        'pmr': True,
        'highchair': False,
        'power': True,
        'wifi': True,
    },
    {
        'number': 6,
        'zone': 'VIP',
        'seats': 2,
        'category': 'VIP',
        'location': 'terrasse',
        'ambiance': 'Romantique, Vue panoramique',
        'pmr': False,
        'highchair': False,
        'power': True,
        'wifi': True,
    },
    {
        'number': 7,
        'zone': 'VIP',
        'seats': 3,
        'category': 'VIP',
        'location': 'intérieur',
        'ambiance': 'Luxe, Éclairage tamisé',
        'pmr': False,
        'highchair': False,
        'power': True,
        'wifi': True,
    },
    # Tables Famille
    {
        'number': 8,
        'zone': 'Standard',
        'seats': 8,
        'category': 'Famille',
        'location': 'intérieur',
        'ambiance': 'Jeux, Couleurs vives',
        'pmr': True,
        'highchair': True,
        'power': True,
        'wifi': True,
    },
    {
        'number': 9,
        'zone': 'Terrasse',
        'seats': 6,
        'category': 'Famille',
        'location': 'terrasse',
        'ambiance': 'Aire de jeux visible',
        'pmr': False,
        'highchair': True,
        'power': False,
        'wifi': True,
    },
    {
        'number': 10,
        'zone': 'Standard',
        'seats': 5,
        'category': 'Famille',
        'location': 'intérieur',
        'ambiance': 'Espace spacieux',
        'pmr': False,
        'highchair': False,
        'power': True,
        'wifi': True,
    },
]

# CREATE NEW TABLES
for data in tables_data:
    table = Table.objects.create(**data)
    print(f'✅ Created Table {table.number}: category={table.category}, location={table.location}')

print(f'\n✅ Total tables created: {Table.objects.count()}')
