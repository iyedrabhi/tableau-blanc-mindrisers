from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'
    
    def ready(self):
        # Importer signals pour que les handlers soient enregistrés
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
