import re
from bs4 import BeautifulSoup
from device import Device


def parse_dhcp_devices(js_content):
    devices = {}
    index = None
    device_name = None

    for line in js_content.splitlines():  # Scansiona riga per riga
        # Cerca l'indice `used_hosts[x-1]!=1`
        index_match = re.search(r"used_hosts\[(\d+)-1]!=1", line)
        if index_match:
            index = int(index_match.group(1))

        # Cerca il nome del dispositivo `selection_list += '<option ...>`
        name_match = re.search(r"selection_list\s*=\s*selection_list\s*\+\s*'<option\s+value=\d+>(.*?)</option>'", line)
        if name_match:
            device_name = name_match.group(1)

        # Aggiungi l'entry al dizionario solo se abbiamo sia `index` che `device_name`
        if index is not None and device_name is not None:
            devices[index] = device_name  # Aggiungi al dizionario
            # Resetta le variabili per il prossimo dispositivo
            index = None
            device_name = None

    return devices


def is_valid_ip(ip):
    """Verifica se una stringa è un indirizzo IP valido."""
    parts = ip.split(".")
    return (
            len(parts) == 4 and
            all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)
    )


def unify_mac(mac):
    """Rimuove i ':' da un MAC address per facilitare i confronti."""
    return mac.replace(":", "").lower()


def extract_mac_from_name(device_name):
    """Estrae il MAC address dal nome del dispositivo se è nel formato 'Unknown-xx-xx-xx-xx-xx-xx'."""
    mac_match = re.search(r'(\b[0-9a-fA-F]{2}(?:-[0-9a-fA-F]{2}){5}\b)', device_name)
    if mac_match:
        return mac_match.group(0).replace("-", ":").lower()  # Converti i "-" in ":" per confronto
    return None


def merge_device_info(dhcp_devices, connected_devices):
    merged_devices = []
    for i in range(1, 10): print("*", end="")
    print("\n\n", dhcp_devices, "\n\n")
    for i in range(1, 10): print("*", end="")

    # Crea un dizionario dal primo set di dati (dispositivi DHCP) con il MAC address unificato come chiave e l'indice e hostname come valori
    dhcp_dict = {}
    for index, device_name in dhcp_devices.items():
        mac_address = extract_mac_from_name(device_name)
        if mac_address:
            dhcp_dict[unify_mac(mac_address)] = (index, device_name)

    # Per ogni dispositivo nel secondo set di dati, trova la corrispondenza nel primo set
    for device in connected_devices:
        mac_key = unify_mac(device.mac_address)
        if mac_key in dhcp_dict:
            # Ottieni index e hostname dal primo set di dati
            index, dhcp_hostname = dhcp_dict[mac_key]
            device.index = index
            # Usa il nome del DHCP se disponibile, altrimenti usa il nome del dispositivo connesso
            device.hostname = dhcp_hostname if dhcp_hostname != "Unknown" else device.hostname
        else:
            # Se non esiste una corrispondenza, assegna "ND" all'index
            device.index = "ND"

        # Aggiungi il dispositivo alla lista finale
        merged_devices.append(device)

    return merged_devices


def parse_device_list(list_html, connection_type):
    devices = []
    for item in list_html.find_all("li", class_="device"):
        name = item.get("name", "Unknown")  # Nome del dispositivo o IP

        # Trova il MAC address
        mac_address = item.get("mac-id", "Unknown")

        # Cerca il primo <span> con la classe 'device-subinfo' che contiene l'indirizzo IP
        ip_address = None
        for span in item.find_all("span", class_="device-subinfo"):
            text = span.get_text(strip=True)
            if is_valid_ip(text):
                ip_address = text
                break

        # Usa 'name' come fallback se l'IP non è stato trovato
        ip_address = ip_address or name
        devices.append(Device(name, ip_address, mac_address, connection_type))
    return devices


def parse_devices(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    devices = []

    # Parsing dei dispositivi connessi via Ethernet
    ethernet_list = soup.find(id="sEthernetList")
    if ethernet_list:
        devices.extend(parse_device_list(ethernet_list, "Ethernet"))

    # Parsing dei dispositivi connessi via WiFi
    wifi_list = soup.find(id="sWifimergeList")
    if wifi_list:
        devices.extend(parse_device_list(wifi_list, "WiFi"))

    # Parsing dei telefoni
    fxs_list = soup.find(id="sFxsList")
    if fxs_list:
        for device in fxs_list.find_all('li', class_='device'):
            name = device.get("name", "Unknown")
            phone_info = device.find("span", class_="pull-right device-subinfo")
            phone_number = phone_info.get_text(strip=True) if phone_info else "Unknown"
            devices.append(Device(name, phone_number, "Unknown", "Telefono"))

    return devices


class DeviceManager:
    def __init__(self, client):
        self.client = client

    def get_devices_from_dhcp(self):
        response = self.client.send_request("tim-dhcp.lp?ip=&phoneType=undefined")
        if response and response.text:  # Verifica se la risposta è valida
            return parse_dhcp_devices(response.text)
        else:
            print("Errore nella richiesta DHCP o contenuto vuoto.")
            return []

    def get_devices_from_devices_lp(self):
        response = self.client.send_request("devices.lp")
        if response and response.text:  # Verifica se la risposta è valida
            return parse_devices(response.text)
        else:
            print("Errore nella richiesta devices.lp o contenuto vuoto.")
            return []

    # Questa funzione unisce i due metodi precedenti per ottenere tutte le informazioni sui dispositivi
    def get_all_devices(self):
        dhcp_devices = self.get_devices_from_dhcp()
        devices_lp_devices = self.get_devices_from_devices_lp()
        return merge_device_info(dhcp_devices, devices_lp_devices)
