class Device:
    def __init__(self, hostname, ip_address, mac_address, connection_type="Unknown"):
        self.index = None
        self.hostname = hostname
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.connection_type = connection_type

    def __repr__(self):
        return f"Device(index={self.index}, hostname={self.hostname}, ip_address={self.ip_address}, mac_address={self.mac_address}, connection_type={self.connection_type})"

