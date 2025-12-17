from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import Reservation, Notification
from tables.models import Table
from django.utils import timezone
from django.db import models

@staff_member_required
def gerant_notifications_list(request):
    """
    Affiche les notifications du gérant (réservations créées, annulées, etc.) avec filtres par type.
    Types: 'CONFIRMATION' | 'ANNULATION'
    """
    # Effacer les notifications si POST
    if request.method == 'POST':
        Notification.objects.filter(recipient_user=request.user).delete()
        messages.success(request, 'Toutes les notifications ont été supprimées')
        return redirect('gerant_notifications')
    
    # Récupérer le filtre demandé (par défaut: tout)
    filter_type = request.GET.get('filter', 'all')
    
    all_notifs = Notification.objects.filter(recipient_user=request.user).order_by('-created_at')
    
    # Grouper par type pour les onglets
    confirmations = all_notifs.filter(notification_type='CONFIRMATION')
    annulations = all_notifs.filter(notification_type='ANNULATION')
    
    # Sélectionner les notifications à afficher selon le filtre
    if filter_type == 'confirmations':
        notifs = confirmations
    elif filter_type == 'annulations':
        notifs = annulations
    else:
        notifs = all_notifs
    
    context = {
        'notifications': notifs,
        'confirmations_count': confirmations.count(),
        'annulations_count': annulations.count(),
        'total_count': all_notifs.count(),
        'active_filter': filter_type,
    }
    # Types that should be considered staff/manager notifications
    context['staff_types'] = ['CONFIRMATION', 'ANNULATION', 'PROLONGATION', 'RELEASE']
    
    return render(request, 'reservations/gerant_notifications.html', context)

@staff_member_required
def all_reservations(request):
    """
    Vue gérant : liste complète des réservations.
    """
    # Show only active/upcoming reservations (status reserved and not past)
    now = timezone.localtime(timezone.now())
    today = now.date()
    current_time = now.time()

    reservations = Reservation.objects.filter(
        status='reserved'
    ).filter(
        models.Q(date__gt=today) | models.Q(date=today, end_time__gt=current_time)
    ).order_by('date', 'start_time')

    return render(request, 'reservations/all_reservations.html', {
        'reservations': reservations
    })

@staff_member_required
def free_table(request, reservation_id):
    """
    Permet au gérant de libérer une table (fin du créneau ou dépassement).
    """
    # Only allow POST to perform the action
    if request.method != 'POST':
        return redirect('all_reservations')

    reservation = get_object_or_404(Reservation, id=reservation_id)
    # Marquer comme terminé lorsque le gérant libère une table
    reservation.status = 'finished'
    reservation.save()
    messages.success(request, 'Table marquée comme terminée.')
    return redirect('all_reservations')

@staff_member_required
def tables_list(request):
    """
    Vue gérant : liste des tables réservées ou disponibles.
    """
    # Show only upcoming/active reservations for manager view
    now = timezone.localtime(timezone.now())
    today = now.date()
    current_time = now.time()

    reservations = Reservation.objects.filter(
        status='reserved'
    ).filter(
        models.Q(date__gt=today) | models.Q(date=today, end_time__gt=current_time)
    ).order_by('date', 'start_time')

    # Compute current table status (reserved / libre) for "now"
    now = timezone.localtime(timezone.now())
    today = now.date()
    current_time = now.time()

    # Get tables that are reserved now OR have future reservations
    # (check if table is occupied now AND any future reservations)
    reserved_now_ids = set(
        Reservation.objects.filter(
            status='reserved',
            date=today,
            start_time__lte=current_time,
            end_time__gt=current_time,
        ).values_list('table_id', flat=True)
    )
    
    # Also get tables with future reservations: any date > today OR later today
    future_reserved_ids = set(
        Reservation.objects.filter(
            status='reserved'
        ).filter(
            models.Q(date__gt=today) | models.Q(date=today, start_time__gt=current_time)
        ).values_list('table_id', flat=True)
    )
    
    reserved_table_ids = reserved_now_ids | future_reserved_ids

    tables = Table.objects.all().order_by('number')
    tables_status = []
    for t in tables:
        status = 'Réservée' if t.id in reserved_table_ids else 'Libre'
        tables_status.append({'table': t, 'status': status})

    return render(request, 'tables/gerant_tables_list.html', {
        'reservations': reservations,
        'tables_status': tables_status,
        'now': now,
    })


@staff_member_required
def history(request):
    """
    Archive / historique des réservations : liste des réservations annulées, terminées ou passées.
    """
    now = timezone.localtime(timezone.now())
    today = now.date()
    current_time = now.time()

    # Réservations annulées OU terminées OU déjà entièrement passées
    past_q = models.Q(date__lt=today) | models.Q(date=today, end_time__lte=current_time)
    status_q = models.Q(status='cancelled') | models.Q(status='finished')

    reservations = Reservation.objects.filter(status_q | past_q).order_by('-date', '-start_time')

    return render(request, 'reservations/history.html', {
        'reservations': reservations,
    })
