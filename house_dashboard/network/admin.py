from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("custom_name", "ip_address", "mac_address", "hostname", "last_seen")
    search_fields = ("custom_name", "hostname", "ip_address", "mac_address")
