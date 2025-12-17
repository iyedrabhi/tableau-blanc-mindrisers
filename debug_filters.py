#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from tables.models import Table

print('='*80)
print('TABLE DATA IN DATABASE - CHECKING FOR FILTER VALUES')
print('='*80)

all_tables = Table.objects.all()
print(f'\nTotal tables: {all_tables.count()}\n')

for t in all_tables:
    print(f'Table ID {t.id}:')
    print(f'  number: {t.number}')
    print(f'  category: "{t.category}"')
    print(f'  location: "{t.location}"')
    print(f'  ambiance: "{t.ambiance}"')
    print(f'  zone: {t.zone}')
    print(f'  PMR={t.pmr}, highchair={t.highchair}, power={t.power}, wifi={t.wifi}')
    print()

print('='*80)
print('DISTINCT VALUES')
print('='*80)
print(f'Categories: {list(Table.objects.values_list("category", flat=True).distinct())}')
print(f'Locations: {list(Table.objects.values_list("location", flat=True).distinct())}')
print(f'Ambiances: {list(Table.objects.values_list("ambiance", flat=True).distinct())}')
print(f'Zones: {list(Table.objects.values_list("zone", flat=True).distinct())}')

print('\n' + '='*80)
print('FILTER TEST - category="VIP"')
print('='*80)
vip = Table.objects.filter(category__iexact='VIP')
print(f'Result count: {vip.count()}')
for t in vip:
    print(f'  - Table {t.number} (ID {t.id})')

print('\n' + '='*80)
print('FILTER TEST - location="intérieur"')
print('='*80)
interior = Table.objects.filter(location__iexact='intérieur')
print(f'Result count: {interior.count()}')
for t in interior:
    print(f'  - Table {t.number} (ID {t.id})')

print('\n' + '='*80)
print('FILTER TEST - category="VIP" AND location="intérieur"')
print('='*80)
combo = Table.objects.filter(category__iexact='VIP', location__iexact='intérieur')
print(f'Result count: {combo.count()}')
for t in combo:
    print(f'  - Table {t.number} (ID {t.id})')

print('\nDone!')
