from dyndns_config import DynDNSConfig
from modem_client import ModemClient
from dhcp_config import DHCPConfig
from device_manager import DeviceManager
from port_forwarding import PortForwardingConfig


def main():
    # Credenziali
    username = "Administrator"
    password = "admin"  # Sostituisci con la tua password

    modem = ModemClient(username, password)
    device_manager = DeviceManager(modem)
    dhcp_config = DHCPConfig(modem)

    # Effettua il login
    try:
        modem.login()
        statip_count = dhcp_config.get_statip_count()

    except Exception as e:
        print("Errore durante il login:", e)
        return

    # Configura il DHCP usando la classe DHCPConfig
    dhcp_config = DHCPConfig(
        client=modem,
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
        static_hosts=[
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "38:94:ed:2f:15:10", "ip_addr": "192.168.1.2"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "c4:2b:44:0d:b5:39", "ip_addr": "192.168.1.3"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "18:31:bf:cb:8e:a1", "ip_addr": "192.168.1.4"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "e0:98:06:b5:0c:62", "ip_addr": "192.168.1.5"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "e8:db:84:c2:5e:18", "ip_addr": "192.168.1.6"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "e0:98:06:b4:e0:d7", "ip_addr": "192.168.1.7"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "a0:d0:5b:b7:c6:34", "ip_addr": "192.168.1.8"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "e0:98:06:b5:0c:62", "ip_addr": "192.168.1.9"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "c4:5b:be:54:62:5c", "ip_addr": "192.168.1.10"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "34:94:54:6b:55:cc", "ip_addr": "192.168.1.11"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "34:94:54:6b:40:e9", "ip_addr": "192.168.1.12"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "e0:98:06:b5:23:10", "ip_addr": "192.168.1.49"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "1c:6f:65:ab:68:37", "ip_addr": "192.168.1.50"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "ec:8a:c4:a2:cf:89", "ip_addr": "192.168.1.98"},
            {"add_obj": "add_on", "host_name": f"{statip_count}", "mac_addr": "9a:48:27:0d:e3:28", "ip_addr": "192.168.1.100"}
        ]
    )

    # Configura il DHCP
    # dhcp_config.configure_dhcp(dhcp_config.to_payload())

    # Configura il DynDNS usando la classe DynDNSConfig
    dyndns_config = DynDNSConfig(
        client=modem,
        enable=True,
        provider="DynDNS.Service.dyndns",
        uname="Rhaegal222",
        pwd="Rhaegal2h2",
        hname="sysVeronica.ns0.it"
    )

    # Invia la configurazione DynDNS
    # dyndns_config.configure_dyndns()

    port_forwarding_rules = [
        {"serviceBox": "27", "protocol": "TCP", "public_start": "20", "public_end": "20", "lan_port": "20",
         "ip_addr": "192.168.1.50", "description": "File Transfer Protocol (FTP) Data"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "21", "public_end": "21", "lan_port": "21",
         "ip_addr": "192.168.1.50", "description": "File Transfer Protocol (FTP) Control"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "22", "public_end": "22", "lan_port": "22",
         "ip_addr": "192.168.1.50", "description": "Secure Shell (SSH)"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "25", "public_end": "25", "lan_port": "25",
         "ip_addr": "192.168.1.50", "description": "Simple Mail Transfer Protocol (SMTP)"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "80", "public_end": "80", "lan_port": "80",
         "ip_addr": "192.168.1.50", "description": "Hypertext Transfer Protocol (HTTP)"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "110", "public_end": "110", "lan_port": "110",
         "ip_addr": "192.168.1.50", "description": "Post Office Protocol v3 (POP3)"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "143", "public_end": "143", "lan_port": "143",
         "ip_addr": "192.168.1.50", "description": "Internet Message Access Protocol (IMAP)"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "443", "public_end": "443", "lan_port": "443",
         "ip_addr": "192.168.1.50", "description": "Hypertext Transfer Protocol Secure (HTTPS)"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "465", "public_end": "465", "lan_port": "465",
         "ip_addr": "192.168.1.50", "description": "Simple Mail Transfer Protocol Secure (SMTPS)"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "587", "public_end": "587", "lan_port": "587",
         "ip_addr": "192.168.1.50", "description": "SMTP Submission"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "631", "public_end": "631", "lan_port": "631",
         "ip_addr": "192.168.1.50", "description": "Internet Printing Protocol (IPP)"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "995", "public_end": "995", "lan_port": "995",
         "ip_addr": "192.168.1.50", "description": "Post Office Protocol Secure (POP3S)"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "993", "public_end": "993", "lan_port": "993",
         "ip_addr": "192.168.1.50", "description": "Internet Message Access Protocol Secure (IMAPS)"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "888", "public_end": "888", "lan_port": "888",
         "ip_addr": "192.168.1.50", "description": "Alternate HTTP"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "4200", "public_end": "4200", "lan_port": "4200",
         "ip_addr": "192.168.1.50", "description": "Angular CLI"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "5432", "public_end": "5432", "lan_port": "5432",
         "ip_addr": "192.168.1.50", "description": "PostgreSQL Database"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "8080", "public_end": "8080", "lan_port": "8080",
         "ip_addr": "192.168.1.50", "description": "Alternate HTTP (8080)"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "19999", "public_end": "19999", "lan_port": "19999",
         "ip_addr": "192.168.1.50", "description": "Netdata Monitoring Tool"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "21202", "public_end": "21202", "lan_port": "21202",
         "ip_addr": "192.168.1.50", "description": "aaPanel Linux Panel"},
        {"serviceBox": "27", "protocol": "TCP", "public_start": "40352", "public_end": "40352", "lan_port": "40352",
         "ip_addr": "192.168.1.50", "description": "Custom Port 40352"}
    ]

    port_forwarding_config = PortForwardingConfig(client=modem, rules=port_forwarding_rules)
    port_forwarding_config.configure_port_forwarding()


if __name__ == "__main__":
    main()
