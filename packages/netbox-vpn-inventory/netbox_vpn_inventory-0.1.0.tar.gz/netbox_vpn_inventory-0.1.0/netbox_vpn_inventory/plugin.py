from extras.plugins import PluginConfig

class NetBoxVpnInventoryConfig(PluginConfig):
    name = "netbox_vpn_inventory"
    verbose_name = "VPN Inventory"
    description = "Gerencia túneis VPN entre dispositivos"
    version = "0.1"
    author = 'Quinta'
    base_url = "vpn"

config = NetBoxVpnInventoryConfig
