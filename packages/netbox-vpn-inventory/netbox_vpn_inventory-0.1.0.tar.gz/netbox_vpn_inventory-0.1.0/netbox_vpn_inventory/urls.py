from django.urls import path
from . import views

urlpatterns = [
    path("", views.VpnTunnelListView.as_view(), name="vpntunnel_list"),
    path("add/", views.VpnTunnelEditView.as_view(), name="vpntunnel_add"),
    path("<int:pk>/", views.VpnTunnelView.as_view(), name="vpntunnel_detail"),
    path("<int:pk>/edit/", views.VpnTunnelEditView.as_view(), name="vpntunnel_edit"),
    path("<int:pk>/delete/", views.VpnTunnelDeleteView.as_view(), name="vpntunnel_delete"),
]
