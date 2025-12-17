from django.shortcuts import render
from datetime import datetime, time
from reservations.models import Reservation
from .models import Table

def tables_list(request):
    """
    Vue gérant : liste des tables avec leur statut actuel.
    """
    now = datetime.now()
    date_today = now.date()
    time_now = now.time()

    tables = Table.objects.all()

    table_status = []
    for table in tables:
        is_reserved = table.reservations.filter(
            status='reserved',
            date=date_today,
            start_time__lt=time_now,
            end_time__gt=time_now
        ).exists()

        table_status.append({
            'table': table,
            'status': 'reserved' if is_reserved else 'non_reserved'
        })

    return render(request, 'tables/tables_list.html', {
        'tables': table_status
    })
