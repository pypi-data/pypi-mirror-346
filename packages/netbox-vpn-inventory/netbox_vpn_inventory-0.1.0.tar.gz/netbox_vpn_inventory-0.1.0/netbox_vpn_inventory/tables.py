import django_tables2 as tables
from .models import VpnTunnel

class VpnTunnelTable(tables.Table):
    name = tables.LinkColumn()
    device_a = tables.Column()
    device_b = tables.Column()
    status = tables.Column()
    vpn_type = tables.Column()

    class Meta:
        model = VpnTunnel
        fields = ("name", "device_a", "device_b", "vpn_type", "status")
