from django.urls import path
from .views import DeviceListView
from . import views

urlpatterns = [
    path("", DeviceListView.as_view(), name="device_list"),
    path("scan/", views.trigger_network_scan, name="scan_network")
]
