from django.urls import path
from reservations.views import accueil


# Import côté client
from .views import (
    available_tables,
    create_reservation,
    my_reservations,
    cancel_reservation,
    client_reminders_list,
    notifications_list,
    notifications_poll,
    set_notification_preferences,
    extend_reservation_view,
)

# Import côté gérant
from .views_gerant import (
    tables_list,
    all_reservations,
    free_table,
    history,
    gerant_notifications_list,
)

urlpatterns = [
    # Côté client
    path('available/', available_tables, name='available_tables'),
    path('create/<int:table_id>/', create_reservation, name='create_reservation'),
    path('my/', my_reservations, name='my_reservations'),
    path('', accueil, name='accueil'),
    path('reminders/', client_reminders_list, name='client_reminders'),
    path('api/notifications/poll/', notifications_poll, name='notifications_poll'),
    path('preferences/', set_notification_preferences, name='notification_preferences'),
    path('extend/<int:reservation_id>/', extend_reservation_view, name='extend_reservation'),

    # Côté gérant (routes du gérant dans l'app reservations)
    path('gerant/', tables_list, name='tables_list'),
    path('gerant/all/', all_reservations, name='all_reservations'),
    path('gerant/free/<int:reservation_id>/', free_table, name='free_table'),
    path('gerant/history/', history, name='reservations_history'),
    path('gerant/notifications/', gerant_notifications_list, name='gerant_notifications'),
    # Annulation côté client
    path('cancel/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
]









#copilot ai
