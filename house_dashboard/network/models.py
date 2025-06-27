from django.db import models


class Device(models.Model):
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True)
    custom_name = models.CharField(max_length=255, blank=True)
    device_type = models.CharField(max_length=100, blank=True)  # e.g., "Laptop", "TV"
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_name or self.hostname or self.ip_address
