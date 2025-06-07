from django.contrib import admin
from .models import Truck, Unloading, Warehouse

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('board_number', 'model', 'max_capacity', 'current_weight', 'sio2_percent', 'fe_percent')
    list_filter = ('model',)
    search_fields = ('board_number',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_weight', 'sio2_percent', 'fe_percent', 'polygon')
    search_fields = ('name',)

@admin.register(Unloading)
class UnloadingAdmin(admin.ModelAdmin):
    list_display = ('truck', 'x', 'y', 'in_poligon')
    search_fields = ('truck__board_number',)
