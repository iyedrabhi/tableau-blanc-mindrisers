from rest_framework import serializers
from .models import Commande, Plate

class PlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plate
        fields = ['id', 'title', 'price']

class CommandeSerializer(serializers.ModelSerializer):
    plates = PlateSerializer(many=True, read_only=True)
    class Meta:
        model = Commande
        fields = ['id', 'customer', 'plates', 'total_price', 'type_commande', 'status', 'qr_code']
        read_only_fields = ['total_price', 'qr_code']