from django.shortcuts import render, redirect, get_object_or_404
from tables.models import Table
from .models import Reservation
#from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, time
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.db.models import Q
from client.models import NotificationPreference
from .models import Notification
from .tasks import extend_reservation
from django.http import JsonResponse
import json

#@login_required
@login_required
def available_tables(request):
    """
    Affiche les tables libres pour le créneau choisi avec filtres avancés et recherche.
    """
    tables_libres = None
    context = {}
    
    if request.method == 'POST':
        date_str = request.POST.get('date', '')
        start_time_str = request.POST.get('start_time', '')
        end_time_str = request.POST.get('end_time', '')
        
        # Récupérer les filtres
        category = request.POST.get('category', '')
        location = request.POST.get('location', '')
        ambiance = request.POST.get('ambiance', '')
        pmr = request.POST.get('pmr', '')
        highchair = request.POST.get('highchair', '')
        power = request.POST.get('power', '')
        wifi = request.POST.get('wifi', '')
        
        # Récupérer la recherche
        search_query = request.POST.get('search', '').strip()
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_obj = datetime.strptime(start_time_str, '%H:%M').time()
            end_obj = datetime.strptime(end_time_str, '%H:%M').time()
            
            # Filtrage initial: tables non réservées sur le créneau
            tables_libres = Table.objects.exclude(
                reservations__status='reserved',
                reservations__date=date_obj,
                reservations__start_time__lt=end_obj,
                reservations__end_time__gt=start_obj
            ).distinct()
            
            # Appliquer la recherche (search by table number, category, ambiance, seats, accessibility)
            if search_query:
                search_lower = search_query.lower()
                query_filter = Q(number__icontains=search_query) | \
                               Q(category__icontains=search_query) | \
                               Q(ambiance__icontains=search_query) | \
                               Q(zone__icontains=search_query) | \
                               Q(seats__icontains=search_query)
                
                # Recherche par accessibilité
                if 'pmr' in search_lower or 'mobilité' in search_lower or 'réduite' in search_lower:
                    query_filter |= Q(pmr=True)
                if 'chaise' in search_lower or 'haute' in search_lower or 'enfant' in search_lower:
                    query_filter |= Q(highchair=True)
                if 'wifi' in search_lower or 'internet' in search_lower:
                    query_filter |= Q(wifi=True)
                if 'électricité' in search_lower or 'electrique' in search_lower or 'prise' in search_lower or 'power' in search_lower:
                    query_filter |= Q(power=True)
                
                tables_libres = tables_libres.filter(query_filter)
            
            # Appliquer les filtres avancés
            if category and category != '':
                tables_libres = tables_libres.filter(category__iexact=category)
            if location and location != '':
                tables_libres = tables_libres.filter(location__iexact=location)
            if ambiance and ambiance != '':
                tables_libres = tables_libres.filter(ambiance__icontains=ambiance)
            if pmr:  # Si coché (checkbox)
                tables_libres = tables_libres.filter(pmr=True)
            if highchair:
                tables_libres = tables_libres.filter(highchair=True)
            if power:
                tables_libres = tables_libres.filter(power=True)
            if wifi:
                tables_libres = tables_libres.filter(wifi=True)
            
            # Passer les filtres au template pour pré-remplissage
            context = {
                'tables': tables_libres,
                'date': date_str,
                'start_time': start_time_str,
                'end_time': end_time_str,
                'filter_category': category,
                'filter_location': location,
                'filter_ambiance': ambiance,
                'filter_pmr': pmr,
                'filter_highchair': highchair,
                'filter_power': power,
                'filter_wifi': wifi,
                'search_query': search_query,
            }
        except ValueError as e:
            messages.error(request, f"Erreur de date/heure: {e}")
            context = {
                'date': date_str,
                'start_time': start_time_str,
                'end_time': end_time_str,
                'search_query': search_query,
            }
    
    return render(request, 'reservations/create_reservation.html', context)


@login_required
def client_reminders_list(request):
    """
    Affiche les rappels intelligents de réservations pour le client.
    
    Smart reminders:
    - Morning (< 12:00): 2 hours before
    - Afternoon/evening (>= 12:00): 4 hours before
    
    Filtres possibles: ?status=all|confirmed|reminders|cancellations
    """
    from django.utils import timezone
    
    # Récupérer le filtre demandé
    status_filter = request.GET.get('status', 'all')
    
    # Notifications du client (rappels, confirmations, annulations)
    # Include standardized notification types. Keep older variants for backward compatibility.
    all_notifs = Notification.objects.filter(
        recipient_user=request.user,
        notification_type__in=['CONFIRMATION', 'RAPPEL', 'ANNULATION', 'client', 'reservation', 'cancel']
    ).order_by('-created_at')
    
    # Appliquer le filtre selon la sélection
    if status_filter == 'confirmed':
        # Seulement les confirmations de réservations
        notifs = all_notifs.filter(
            notification_type__in=['CONFIRMATION', 'reservation']
        )
    elif status_filter == 'reminders':
        # Seulement les rappels
        notifs = all_notifs.filter(
            notification_type__in=['RAPPEL', 'client']
        )
    elif status_filter == 'cancellations':
        # Seulement les annulations
        notifs = all_notifs.filter(
            notification_type__in=['ANNULATION', 'cancel']
        )
    else:
        # Tous les filtres
        notifs = all_notifs
    
    # Compter par type (toujours sur all_notifs pour les compteurs)
    confirmations_count = all_notifs.filter(
        notification_type__in=['CONFIRMATION', 'reservation']
    ).count()
    reminders_count = all_notifs.filter(
        notification_type__in=['RAPPEL', 'client']
    ).count()
    cancellations_count = all_notifs.filter(
        notification_type__in=['ANNULATION', 'cancel']
    ).count()
    
    context = {
        'notifications': notifs,
        'confirmations_count': confirmations_count,
        'reminders_count': reminders_count,
        'cancellations_count': cancellations_count,
        'total_count': all_notifs.count(),
        'active_filter': status_filter,
        # Also include any pending scheduled reminders (Reservation objects)
        'pending_reminders': Reservation.objects.filter(
            client=request.user,
            reminder_datetime__isnull=False,
            reminder_sent=False
        ).order_by('reminder_datetime')
    }

    # Provide reusable type groups for templates (avoids tuple literal parsing issues)
    context['confirmation_types'] = ['client', 'reservation', 'CONFIRMATION']
    context['reminder_types'] = ['RAPPEL', 'client']
    context['cancellation_types'] = ['ANNULATION', 'cancel']
    
    return render(request, 'reservations/client_reminders.html', context)


@login_required
def notifications_list(request):
    """Affiche les notifications in-app pour l'utilisateur connecté."""
    # Effacer les notifications si POST
    if request.method == 'POST':
        Notification.objects.filter(recipient_user=request.user).delete()
        messages.success(request, 'Toutes les notifications ont été supprimées')
        return redirect('notifications_list')
    
    notifs = Notification.objects.filter(recipient_user=request.user).order_by('-created_at')
    return render(request, 'reservations/notifications.html', {'notifications': notifs})


@login_required
def set_notification_preferences(request):
    try:
        pref = request.user.notification_pref
    except Exception:
        pref = None

    if request.method == 'POST':
        email_reminders = bool(request.POST.get('email_reminders'))
        sms_reminders = bool(request.POST.get('sms_reminders'))
        inapp_reminders = bool(request.POST.get('inapp_reminders'))
        if pref is None:
            NotificationPreference.objects.create(
                user=request.user,
                email_reminders=email_reminders,
                sms_reminders=sms_reminders,
                inapp_reminders=inapp_reminders
            )
        else:
            pref.email_reminders = email_reminders
            pref.sms_reminders = sms_reminders
            pref.inapp_reminders = inapp_reminders
            pref.save()

        messages.success(request, 'Préférences mises à jour')
        return redirect('my_reservations')

    return render(request, 'reservations/preferences.html', {'pref': pref})
#@login_required
@login_required
def create_reservation(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
    start_time = datetime.strptime(request.POST['start_time'], '%H:%M').time()
    end_time = datetime.strptime(request.POST['end_time'], '%H:%M').time()
    # Check for conflicting reservations on this table for the requested slot
    conflict_exists = Reservation.objects.filter(
        table=table,
        status='reserved',
        date=date,
        start_time__lt=end_time,
        end_time__gt=start_time
    ).exists()

    if conflict_exists:
        messages.error(request, 'Table déjà réservée !')
        return redirect('available_tables')
    # Compute duration in minutes from start/end if provided; fallback to default 90
    try:
        delta = datetime.combine(date, end_time) - datetime.combine(date, start_time)
        duration_minutes = int(delta.total_seconds() // 60)
        if duration_minutes <= 0:
            duration_minutes = 90
    except Exception:
        duration_minutes = 90

    # Calculate smart reminder time based on reservation time
    # If start_time < 12:00 (morning): remind 2 hours before
    # If start_time >= 12:00 (afternoon/evening): remind 4 hours before
    from datetime import timedelta as dt_delta
    reminder_lead = 2 if start_time.hour < 12 else 4
    reminder_datetime = timezone.make_aware(
        datetime.combine(date, start_time) - dt_delta(hours=reminder_lead)
    )

    reservation = Reservation.objects.create(
        client=request.user,
        table=table,
        date=date,
        start_time=start_time,
        end_time=end_time,
        duration_minutes=duration_minutes,
        reminder_datetime=reminder_datetime
    )

    # Mark synthetic flag on the table for quick queries
    table.is_reserved = True
    table.save(update_fields=['is_reserved'])

    # Send notifications to managers and client
    from .services.notifications import create_inapp_notification
    from client.models import CustomUser

    # Notify all managers/staff
    staff_users = CustomUser.objects.filter(is_staff=True)
    for staff in staff_users:
        create_inapp_notification(
            staff,
            f"📅 Nouvelle réservation - Table {table.number}",
            f"Table {table.number} réservée par {request.user.username} pour le {date} à {start_time}",
            notification_type='CONFIRMATION'
        )

    # Notify client
    create_inapp_notification(
        request.user,
        f"✅ Réservation confirmée - Table {table.number}",
        f"Votre réservation pour la table {table.number} le {date} à {start_time} est confirmée.",
        notification_type='CONFIRMATION'
    )

    messages.success(request, 'Réservation créée avec succès.')
    return redirect('my_reservations')
#@login_required
@login_required
def my_reservations(request):
    reservations = request.user.reservations.all().order_by('-date', '-start_time')
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})


@login_required
def extend_reservation_view(request, reservation_id):
    """Action du client pour demander une prolongation (minutes fournies via POST)."""
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.client != request.user:
        messages.error(request, "Action non autorisée.")
        return redirect('my_reservations')

    if request.method == 'POST':
        extra = int(request.POST.get('extra_minutes', 30))
        extend_reservation.delay(reservation.id, extra)
        messages.success(request, f'Prolongation demandée de {extra} minutes. Le gérant sera notifié.')
        return redirect('my_reservations')

    return render(request, 'reservations/extend_confirm.html', {'reservation': reservation})


#@login_required
@login_required
def cancel_reservation(request, reservation_id):
    """
    Permet au client d'annuler sa réservation avant le début du créneau.
    Change le statut en 'cancelled' si l'utilisateur est le propriétaire et
    que le créneau n'a pas encore commencé.
    """
    from .services.notifications import create_inapp_notification
    from client.models import CustomUser
    
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Vérifier que l'utilisateur est bien le client
    if reservation.client != request.user:
        messages.error(request, "Action non autorisée.")
        return redirect('my_reservations')

    # Use timezone-aware comparison (project uses USE_TZ=True)
    now = timezone.localtime(timezone.now())
    today = now.date()
    current_time = now.time()

    # If reservation date is in the past, or it's today and start_time already passed, disallow
    if reservation.date < today or (reservation.date == today and reservation.start_time <= current_time):
        messages.error(request, "Impossible d'annuler: le créneau est déjà commencé ou passé.")
        return redirect('my_reservations')

    # Annuler la réservation
    reservation.status = 'cancelled'
    reservation.save()

    # Notify client of cancellation
    create_inapp_notification(
        request.user,
        f"Réservation annulée",
        f"Votre réservation pour la table {reservation.table.number} le {reservation.date} à {reservation.start_time} a été annulée.",
        notification_type='ANNULATION'
    )

    # Notify all staff members
    staff_users = CustomUser.objects.filter(is_staff=True)
    for staff in staff_users:
        create_inapp_notification(
            staff,
            f"❌ Annulation - Table {reservation.table.number}",
            f"La réservation de {reservation.client.username} (table {reservation.table.number}) le {reservation.date} à {reservation.start_time} a été annulée.",
            notification_type='ANNULATION'
        )

    messages.success(request, "Réservation annulée avec succès.")
    return redirect('my_reservations')
def simple_login(request):
    message = ""
    # ensure a CSRF cookie/token is set for the response (helps avoid mismatches)
    get_token(request)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # rediriger selon rôle
            if user.is_staff:  # gérant
                return redirect('gerant')
            else:  # client
                return redirect('accueil')
        else:
            message = "Nom d'utilisateur ou mot de passe incorrect."
    return render(request, 'login.html', {'message': message})

def simple_logout(request):
    logout(request)
    return redirect('/')

def accueil(request):
    return render(request, 'menu.html')


@login_required
def notifications_poll(request):
    """JSON endpoint to poll recent notifications for the logged-in user.

    Accepts optional query param `since` (integer milliseconds since epoch). Returns
    list of notifications newer than `since`. This is a fallback for environments
    where WebSockets (Daphne) are not running.
    """
    since = request.GET.get('since')
    qs = Notification.objects.filter(recipient_user=request.user).order_by('-created_at')
    if since:
        try:
            since_ms = int(since)
            since_dt = timezone.datetime.fromtimestamp(since_ms / 1000.0, tz=timezone.utc)
            qs = qs.filter(created_at__gt=since_dt)
        except Exception:
            pass

    notifs = []
    for n in qs[:50]:
        # created_at to milliseconds
        ts = int(n.created_at.timestamp() * 1000)
        notifs.append({
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.notification_type,
            'ts': ts,
        })

    return JsonResponse({'notifications': notifs})


