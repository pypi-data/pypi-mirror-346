from extras.jobs import Job
from dcim.models import Device
from .models import VpnTunnel
import requests

class UpdateVpnStatusJob(Job):
    class Meta:
        name = "Atualizar Status dos Túneis (FortiOS)"

    def run(self, data, commit):
        for tunnel in VpnTunnel.objects.all():
            try:
                forti_ip = tunnel.endpoint_a_ip
                api_url = f"https://{forti_ip}/api/v2/monitor/vpn/ipsec/phase2/select"
                headers = {"Authorization": "Bearer SEU_TOKEN"}
                response = requests.get(api_url, verify=False, headers=headers, timeout=5)

                if response.status_code == 200 and "tunnel" in response.text:
                    tunnel.status = "up"
                else:
                    tunnel.status = "down"

                if commit:
                    tunnel.save()
                self.log_info(f"Atualizado túnel {tunnel.name}: {tunnel.status}")

            except Exception as e:
                tunnel.status = "unknown"
                self.log_failure(f"Erro ao verificar túnel {tunnel.name}: {str(e)}")

                if commit:
                    tunnel.save()
