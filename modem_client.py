import requests
import hashlib


class ModemClient:
    BASE_URL = "http://192.168.1.1"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def get_preauth(self):
        """Effettua la richiesta di pre-autenticazione e restituisce i parametri ottenuti."""
        pre_auth_url = f"{self.BASE_URL}/login.lp?get_preauth=true"
        response = self.session.get(pre_auth_url)
        if response.status_code == 200:
            pre_auth_data = response.text.split('|')
            rn, realm, nonce, qop = pre_auth_data[0], pre_auth_data[1], pre_auth_data[2], pre_auth_data[3]
            return rn, realm, nonce, qop
        else:
            raise Exception(f"Errore durante il pre-auth: {response.status_code}")

    def calculate_hidepw(self, realm, nonce, qop):
        """Calcola l'hash della password per il campo hidepw usando MD5."""
        ha1 = hashlib.md5(f"{self.username}:{realm}:{self.password}".encode()).hexdigest()
        ha2 = hashlib.md5("GET:/login.lp".encode()).hexdigest()
        hidepw = hashlib.md5(f"{ha1}:{nonce}:00000001:xyz:{qop}:{ha2}".encode()).hexdigest()
        return hidepw

    def login(self):
        """Effettua il login al modem."""
        rn, realm, nonce, qop = self.get_preauth()
        hidepw = self.calculate_hidepw(realm, nonce, qop)
        login_url = f"{self.BASE_URL}/login.lp"
        login_data = {
            "rn": rn,
            "user": self.username,
            "hidepw": hidepw
        }
        response = self.session.post(login_url, data=login_data)
        if response.status_code == 200:
            print("Login effettuato con successo")
            return True
        else:
            raise Exception(f"Errore durante il login: {response.status_code}")

    def send_request(self, endpoint, method="GET", data=None):
        url = f"{self.BASE_URL}/{endpoint}"
        if method == "GET":
            response = self.session.get(url)
        elif method == "POST":
            response = self.session.post(url, data=data)
        else:
            raise ValueError("Metodo HTTP non supportato")

        response.raise_for_status()  # Solleva un’eccezione in caso di errore
        return response
