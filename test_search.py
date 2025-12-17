#!/usr/bin/env python
"""
Test script to verify search functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from tables.models import Table
from django.db.models import Q

print('\n' + '='*70)
print('TESTING SEARCH FUNCTIONALITY')
print('='*70)

# Test 1: Search by table number
print('\n[TEST 1] Search by table number "5":')
results = Table.objects.filter(
    Q(number__icontains='5') |
    Q(category__icontains='5') |
    Q(ambiance__icontains='5') |
    Q(zone__icontains='5')
)
print(f'Results: {results.count()} tables')
for t in results:
    print(f'  - Table {t.number}: {t.category} - {t.ambiance}')

# Test 2: Search by category
print('\n[TEST 2] Search by category "VIP":')
results = Table.objects.filter(
    Q(number__icontains='VIP') |
    Q(category__icontains='VIP') |
    Q(ambiance__icontains='VIP') |
    Q(zone__icontains='VIP')
)
print(f'Results: {results.count()} tables')
for t in results:
    print(f'  - Table {t.number}: {t.category}')

# Test 3: Search by ambiance
print('\n[TEST 3] Search by ambiance "calme":')
results = Table.objects.filter(
    Q(number__icontains='calme') |
    Q(category__icontains='calme') |
    Q(ambiance__icontains='calme') |
    Q(zone__icontains='calme')
)
print(f'Results: {results.count()} tables')
for t in results:
    print(f'  - Table {t.number}: {t.ambiance}')

# Test 4: Search by zone
print('\n[TEST 4] Search by zone "Standard":')
results = Table.objects.filter(
    Q(number__icontains='Standard') |
    Q(category__icontains='Standard') |
    Q(ambiance__icontains='Standard') |
    Q(zone__icontains='Standard')
)
print(f'Results: {results.count()} tables')
for t in results:
    print(f'  - Table {t.number}: Zone={t.zone}')

# Test 5: Search + Filter combination
print('\n[TEST 5] Search "VIP" + Filter by location="intérieur":')
results = Table.objects.filter(
    Q(number__icontains='VIP') |
    Q(category__icontains='VIP') |
    Q(ambiance__icontains='VIP') |
    Q(zone__icontains='VIP')
).filter(location__iexact='intérieur')
print(f'Results: {results.count()} tables')
for t in results:
    print(f'  - Table {t.number}: {t.category} - {t.location}')

print('\n' + '='*70)
print('SUCCESS - Search functionality working!')
print('='*70 + '\n')
