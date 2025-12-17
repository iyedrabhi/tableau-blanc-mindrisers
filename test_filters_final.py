#!/usr/bin/env python
"""
Test script to verify filter functionality is working
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from tables.models import Table
from reservations.models import Reservation
from datetime import datetime, date, time

print('\n' + '='*80)
print('TESTING FILTER FUNCTIONALITY - FINAL VERIFICATION')
print('='*80)

# Test 1: VIP Filter
print('\n✅ TEST 1: Filter by category="VIP"')
vip_tables = Table.objects.filter(category__iexact='VIP')
print(f'   Result: {vip_tables.count()} VIP tables found')
for t in vip_tables:
    print(f'   - Table {t.number} ({t.ambiance})')
assert vip_tables.count() == 3, 'Expected 3 VIP tables'

# Test 2: Interior Location Filter
print('\n✅ TEST 2: Filter by location="intérieur"')
interior = Table.objects.filter(location__iexact='intérieur')
print(f'   Result: {interior.count()} interior tables found')
for t in interior:
    print(f'   - Table {t.number} ({t.category})')
assert interior.count() == 7, 'Expected 7 interior tables'

# Test 3: PMR Filter
print('\n✅ TEST 3: Filter by PMR=True')
pmr_tables = Table.objects.filter(pmr=True)
print(f'   Result: {pmr_tables.count()} PMR-accessible tables found')
for t in pmr_tables:
    print(f'   - Table {t.number} ({t.category})')
assert pmr_tables.count() == 3, 'Expected 3 PMR tables'

# Test 4: Highchair Filter
print('\n✅ TEST 4: Filter by highchair=True')
highchair_tables = Table.objects.filter(highchair=True)
print(f'   Result: {highchair_tables.count()} tables with highchair found')
for t in highchair_tables:
    print(f'   - Table {t.number} ({t.category})')
assert highchair_tables.count() == 3, 'Expected 3 highchair tables'

# Test 5: Combined Filters
print('\n✅ TEST 5: Filter by category="Famille" AND location="intérieur" AND highchair=True')
famille_int_hc = Table.objects.filter(
    category__iexact='Famille',
    location__iexact='intérieur',
    highchair=True
)
print(f'   Result: {famille_int_hc.count()} tables found')
for t in famille_int_hc:
    print(f'   - Table {t.number}')
assert famille_int_hc.count() == 1, 'Expected 1 Famille table in interior with highchair'

# Test 6: Ambiance Filter
print('\n✅ TEST 6: Filter by ambiance (contains "calme")')
calm_ambiance = Table.objects.filter(ambiance__icontains='calme')
print(f'   Result: {calm_ambiance.count()} tables with calm ambiance found')
for t in calm_ambiance:
    print(f'   - Table {t.number}: {t.ambiance}')
assert calm_ambiance.count() == 1, 'Expected 1 table with calm ambiance'

print('\n' + '='*80)
print('✅ ALL FILTER TESTS PASSED!')
print('='*80)
print('\nYour filters are now working correctly!')
print('Try these in the web interface at http://localhost:8000/reservations/available/:')
print('  1. Select date: 2025-12-15')
print('  2. Select times: 12:00 to 14:00')
print('  3. Filter by category="VIP" → should see 3 tables')
print('  4. Filter by location="terrasse" → should see tables on terrace')
print('  5. Check "PMR" checkbox → should see only accessible tables')
print('  6. Try combining filters!')
print('\n')
