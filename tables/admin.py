from django.contrib import admin

# Register your models here.

from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'zone', 'seats')
