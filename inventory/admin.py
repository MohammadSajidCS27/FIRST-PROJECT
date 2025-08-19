from django.contrib import admin
from .models import Location, InventoryItem


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("identifier", "name", "category", "location", "quantity")
    list_filter = ("category", "location")
    search_fields = ("identifier", "name")
