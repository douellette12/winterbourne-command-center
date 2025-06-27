from django.core.management.base import BaseCommand
from ...utils import scan_network

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        scan_network()
        self.stdout.write("LAN scan completed.")
