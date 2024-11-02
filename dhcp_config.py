class DHCPConfig:
    def __init__(self,
                 client,
                 mode="ADVANCED",
                 enable=True,
                 gateway="192.168.1.1",
                 gateway_parts=("192", "168", "1", "1"),
                 subnet_mask="255.255.255.0",
                 subnet_mask_parts=("255", "255", "255", "0"),
                 min_ip="192.168.1.2",
                 min_ip_parts=("192", "168", "1", "2"),
                 max_ip="192.168.1.254",
                 max_ip_parts=("192", "168", "1", "254"),
                 lease_time=21600,
                 gw_ip="192.168.1.1",
                 pre_def_stat_ip="0",
                 static_hosts=None):
        # Configurazione di base
        self.client = client
        self.mode = mode
        self.enable = enable
        self.gateway = gateway
        self.gateway_parts = gateway_parts
        self.subnet_mask = subnet_mask
        self.subnet_mask_parts = subnet_mask_parts
        self.min_ip = min_ip
        self.min_ip_parts = min_ip_parts
        self.max_ip = max_ip
        self.max_ip_parts = max_ip_parts
        self.lease_time = lease_time
        self.gw_ip = gw_ip
        self.pre_def_stat_ip = pre_def_stat_ip
        self.statip_count = self.get_statip_count()
        self.static_hosts = static_hosts or []

    def to_payload(self):
        """Converte la configurazione in un dizionario per l'invio della richiesta."""
        payload = {
            # Modalità e abilitazione
            "DHCPv4_MODE": self.mode,
            "dhcp_enable": "1" if self.enable else "0",

            # Gateway principale
            "IP_AM": self.gateway,
            "IP_AM1": self.gateway_parts[0],
            "IP_AM2": self.gateway_parts[1],
            "IP_AM3": self.gateway_parts[2],
            "IP_AM4": self.gateway_parts[3],

            # Maschera di sottorete
            "DHCP_SM": self.subnet_mask,
            "DHCP_SM1": self.subnet_mask_parts[0],
            "DHCP_SM2": self.subnet_mask_parts[1],
            "DHCP_SM3": self.subnet_mask_parts[2],
            "DHCP_SM4": self.subnet_mask_parts[3],

            # Intervallo di IP
            "DHCP_MinIP": self.min_ip,
            "DHCP_MinIP1": self.min_ip_parts[0],
            "DHCP_MinIP2": self.min_ip_parts[1],
            "DHCP_MinIP3": self.min_ip_parts[2],
            "DHCP_MinIP4": self.min_ip_parts[3],

            "DHCP_MaxIP": self.max_ip,
            "DHCP_MaxIP1": self.max_ip_parts[0],
            "DHCP_MaxIP2": self.max_ip_parts[1],
            "DHCP_MaxIP3": self.max_ip_parts[2],
            "DHCP_MaxIP4": self.max_ip_parts[3],

            # Durata del lease
            "DHCP_LTime": str(self.lease_time),

            # IP del Gateway
            "GW_IP": self.gw_ip,

            # Impostazioni per IP statici
            "pre_def_stat_ip": self.pre_def_stat_ip,
            "statip_count": self.statip_count
        }

        # Aggiunta degli host statici
        for idx, host in enumerate(self.static_hosts, start=1):
            payload[f"add_obj{idx}"] = host.get("add_obj", "add_on")
            payload[f"host_name{idx}"] = host.get("host_name", "")  # Nome host
            payload[f"mac_addr{idx}"] = host.get("mac_addr", "")  # MAC address
            payload[f"ip_addr{idx}"] = host.get("ip_addr", "")  # Indirizzo IP

        return payload

    def configure_dhcp(self, payload):
        print("Invio della configurazione DHCP...")
        print(payload)
        response = self.client.send_request("/tim-dhcp.lp", method="POST", data=payload)
        if response.status_code == 200:
            print("Configurazione DHCP inviata con successo.")
        else:
            raise Exception(f"Errore durante l'invio della configurazione DHCP: {response.status_code}")

    def get_statip_count(self):
        response = self.client.send_request("/tim-dhcp.lp?ip=&phoneType=undefined")
        js_content = response.text  # Ottieni il contenuto della risposta

        cur_sel_count = 0
        for line in js_content.splitlines():
            # Cerca 'cur_sel' nella riga corrente
            if 'cur_sel' in line:
                cur_sel_count += 1

        return cur_sel_count - 1
