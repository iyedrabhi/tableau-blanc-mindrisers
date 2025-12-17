from django import template
from CommandesApp.models import Plate

register = template.Library()

@register.filter
def get_plate_image(plate_id):
    """Retourne l'URL de l'image d'un plat"""
    try:
        plate = Plate.objects.get(pk=plate_id)
        return plate.image.url if plate.image else ''
    except Plate.DoesNotExist:
        return ''

@register.filter
def get_plate_price(plate_id):
    """Retourne le prix d'un plat"""
    try:
        plate = Plate.objects.get(pk=plate_id)
        return plate.price
    except Plate.DoesNotExist:
        return 0
