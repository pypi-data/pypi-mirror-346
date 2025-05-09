from netbox.views import generic
from . import models, forms, tables, filters

class VpnTunnelListView(generic.ObjectListView):
    queryset = models.VpnTunnel.objects.all()
    table = tables.VpnTunnelTable
    filterset = filters.VpnTunnelFilter

class VpnTunnelView(generic.ObjectView):
    queryset = models.VpnTunnel.objects.all()

class VpnTunnelEditView(generic.ObjectEditView):
    queryset = models.VpnTunnel.objects.all()
    model_form = forms.VpnTunnelForm

class VpnTunnelDeleteView(generic.ObjectDeleteView):
    queryset = models.VpnTunnel.objects.all()
