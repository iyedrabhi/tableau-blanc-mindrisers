from django.contrib import admin
from django.utils.html import format_html
from .models import Commande, Menu, Plate


admin.site.site_header = "Administration des Commandes"
admin.site.site_title = "CommandesApp Admin Portal"
admin.site.index_title = "Bienvenue dans le portail d'administration CommandesApp"


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "created_at", "display_qr")
    list_filter = ("status", "type_commande")
    search_fields = ("customer__username", "id")
    readonly_fields = ("qr_code", "created_at", "total_price")

    def display_qr(self, obj):
        if obj.qr_code:
            return format_html("<img src='{}' width='80' />", obj.qr_code.url)
        return "Aucun QR"
    display_qr.short_description = "QR Code"


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("title", "get_plates")

    def get_plates(self, obj):
        return ", ".join([p.title for p in obj.plates.all()])
    get_plates.short_description = "Plats"


@admin.register(Plate)
class PlateAdmin(admin.ModelAdmin):
    list_display = ("title", "price","image")
    search_fields = ("title",)
