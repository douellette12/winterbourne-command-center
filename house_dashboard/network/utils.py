import nmap
import socket
from .models import Device

def scan_network(subnet="192.168.0.0/24"):
    scanner = nmap.PortScanner()
    scanner.scan(hosts=subnet, arguments='-sn -PR -R')

    for host in scanner.all_hosts():
        ip = scanner[host]['addresses'].get('ipv4')
        mac = scanner[host]['addresses'].get('mac', '')

        # Try to get hostname from nmap, then fallback to reverse DNS
        hostname = ''
        try:
            if scanner[host]['hostnames']:
                hostname = scanner[host]['hostnames'][0]['name']
            if not hostname:
                hostname = socket.gethostbyaddr(ip)[0]
                print(hostname)
        except Exception:
            hostname = ''

        if ip:
            device, _ = Device.objects.update_or_create(
                ip_address=ip,
                defaults={
                    'mac_address': mac,
                    'hostname': hostname,
                }
            )
