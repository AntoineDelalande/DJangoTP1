from django.contrib import admin
from .models import Location, Vehicle

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_filter = ["location"]
    search_fields = ["number"]
    pass