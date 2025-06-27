from django.views.generic import ListView
from .models import Device
from django.core.management import call_command
from django.shortcuts import redirect
from django.contrib import messages


def trigger_network_scan(request):
    if request.method == "POST":
        try:
            call_command("scan_lan")  # this is your existing management command
            messages.success(request, "Network scan completed.")
        except Exception as e:
            messages.error(request, f"Scan failed: {e}")
    return redirect("device_list")  # Change to your list page's name


class DeviceListView(ListView):
    model = Device
    context_object_name = "devices"
