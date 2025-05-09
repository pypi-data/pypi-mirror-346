import django_filters
from .models import VpnTunnel

class VpnTunnelFilter(django_filters.FilterSet):
    class Meta:
        model = VpnTunnel
        fields = ["status", "vpn_type", "device_a", "device_b"]
