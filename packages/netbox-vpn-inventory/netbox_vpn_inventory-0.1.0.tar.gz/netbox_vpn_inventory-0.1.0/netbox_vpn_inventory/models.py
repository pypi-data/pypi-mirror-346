from django.db import models
from netbox.models import NetBoxModel
from dcim.models import Device

class VpnTunnel(NetBoxModel):
    name = models.CharField(max_length=100, unique=True)
    device_a = models.ForeignKey(Device, related_name='vpn_end_a', on_delete=models.PROTECT)
    device_b = models.ForeignKey(Device, related_name='vpn_end_b', on_delete=models.PROTECT)
    endpoint_a_ip = models.GenericIPAddressField()
    endpoint_b_ip = models.GenericIPAddressField()
    vpn_type = models.CharField(max_length=50, choices=[("ipsec", "IPSec"), ("ssl", "SSL"), ("gre", "GRE")])
    status = models.CharField(max_length=20, choices=[("up", "Up"), ("down", "Down"), ("unknown", "Unknown")], default="unknown")

    def __str__(self):
        return self.name
