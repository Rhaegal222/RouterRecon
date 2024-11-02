class DynDNSConfig:
    def __init__(self, client, enable=True, provider="DynDNS.Service.dyndns", uname="", pwd="", hname=""):
        self.client = client
        self.enable = enable
        self.provider = provider
        self.uname = uname
        self.pwd = pwd
        self.hname = hname
        self.ser_port = "80"  # Porta predefinita per il servizio

    def to_payload(self):
        """Converte la configurazione in un dizionario per l'invio della richiesta."""
        payload = {
            "on": "1" if self.enable else "0",
            "provider": self.provider,
            "uname": self.uname,
            "pwd": self.pwd,
            "hname": self.hname,
            "ser_server": "",
            "ser_port": self.ser_port,
            "ser_req": "",
            "ser_up": "0",
            "ser_ret": "0",
            "ser_max": "0"
        }
        return payload

    def configure_dyndns(self):
        """Invia la configurazione DynDNS al modem."""
        payload = self.to_payload()
        print("Invio della configurazione DynDNS...")
        print(payload)
        response = self.client.send_request("/tim-dyndns.lp", method="POST", data=payload)
        if response.status_code == 200:
            print("Configurazione DynDNS inviata con successo.")
        else:
            raise Exception(f"Errore durante l'invio della configurazione DynDNS: {response.status_code}")
