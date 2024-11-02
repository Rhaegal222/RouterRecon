class PortForwardingConfig:
    def __init__(self, client, rules, nat_min_ip="192.168.1.2", nat_max_ip="192.168.1.254"):
        """
        Configura le regole di port forwarding.
        :param client: Istanza di ModemClient per inviare le richieste.
        :param rules: Lista di dizionari contenenti le regole di port forwarding.
        """
        self.client = client
        self.rules = rules  # Ogni regola è un dizionario con i dettagli della configurazione.
        self.nat_min_ip = nat_min_ip
        self.nat_max_ip = nat_max_ip

    def to_payload(self):
        """Converte le regole di port forwarding in un dizionario per l'invio della richiesta."""
        payload = {
            "NAT_MODE": "",
            "natconf_enable": "enabled",
            "NAT_MinIP": self.nat_min_ip,
            "NAT_MinIP1": self.nat_min_ip.split(".")[0],
            "NAT_MinIP2": self.nat_min_ip.split(".")[1],
            "NAT_MinIP3": self.nat_min_ip.split(".")[2],
            "NAT_MinIP4": self.nat_min_ip.split(".")[3],
            "NAT_MaxIP": self.nat_max_ip,
            "NAT_MaxIP1": self.nat_max_ip.split(".")[0],
            "NAT_MaxIP2": self.nat_max_ip.split(".")[1],
            "NAT_MaxIP3": self.nat_max_ip.split(".")[2],
            "NAT_MaxIP4": self.nat_max_ip.split(".")[3],
            "PMGW": "0",
            "PMGW1": "0",
            "row_count": str(len(self.rules))
        }

        # Aggiungi le regole di port forwarding specifiche
        for idx, rule in enumerate(self.rules, start=1):
            payload[f"add_obj{idx}"] = "add_on"
            payload[f"del_obj_check{idx}"] = "del_off"
            payload[f"Active_{idx}"] = "0"
            payload[f"serviceBox{idx}"] = "27"  # Fissato a 27 come richiesto
            payload[f"Protocol_{idx}"] = rule.get("protocol", "Any")
            payload[f"PublicStart_{idx}"] = rule.get("public_start", "")
            payload[f"PublicEnd_{idx}"] = rule.get("public_end", "")
            payload[f"LanPort_{idx}"] = rule.get("lan_port", "")
            payload[f"IPAddr_{idx}"] = rule.get("ip_addr", "")
            payload[f"Desc_{idx}"] = rule.get("description", f"Rule {idx}")

        return payload

    def configure_port_forwarding(self):
        """Invia la configurazione di port forwarding al modem."""
        payload = self.to_payload()
        print("Invio della configurazione di port forwarding...")
        print(payload)
        response = self.client.send_request("/accesscontrol-nat.lp", method="POST", data=payload)
        if response.status_code == 200:
            print("Configurazione di port forwarding inviata con successo.")
        else:
            raise Exception(f"Errore durante l'invio della configurazione di port forwarding: {response.status_code}")
