# Technicolor TIM Modem Management Tool

This project is a Python-based tool designed for the management and configuration of the Technicolor TIM modem (Model AGCOMBO, as shown in the uploaded image). It provides automation for various network management tasks, such as retrieving connected device information, configuring DHCP, setting up DynDNS, and managing port forwarding rules.

## Features

1. **Device Management**:
   - Retrieve information about connected devices via DHCP or Ethernet/WiFi connections.
   - The tool collects device names, IP addresses, and MAC addresses, and unifies this information for easy management.

2. **DHCP Configuration**:
   - Set DHCP configurations, including gateway, subnet mask, and IP range.
   - Allows configuration of static IPs within the specified range for devices on the network.

3. **DynDNS Setup**:
   - Configures DynDNS service to keep a hostname dynamically linked to the modem's WAN IP, enabling remote access with a consistent hostname.

4. **Port Forwarding**:
   - Automates the configuration of port forwarding rules, mapping specific public ports to local IP addresses and ports to make internal services accessible externally.

5. **Modem Connection Interface**:
   - The `ModemClient` class handles connection and authentication with the modem using password hashing and session management, allowing it to retrieve or push configurations.

6. **Automatic Dependency Installation**:
   - Checks for required libraries (`requests` and `beautifulsoup4`) and installs them if not already present.

## Requirements

- **Python 3.x**
- Required Python libraries are listed in `requirements.txt`:
  - `requests`
  - `beautifulsoup4`

Use the following command to install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Technicolor-TIM-Modem-Management.git
   cd Technicolor-TIM-Modem-Management
   ```

2. **Install Dependencies**:
   ```bash
   python install_requirements.py
   ```

3. **Run the Script**:
   - Modify `main.py` with your modem's credentials and any specific configurations (e.g., DHCP settings, DynDNS details, and port forwarding rules).
   - Run the main script:
   ```bash
   python main.py
   ```

## Configuration Details

The configuration options available in this tool cover the following areas:

- **DHCP Configuration**: Customizable settings for gateway, subnet mask, and lease duration, as well as optional static IP assignments.
- **DynDNS**: Supports automatic updates to DynDNS service providers to keep a consistent hostname.
- **Port Forwarding Rules**: Allows specifying protocol, public ports, LAN ports, and IP addresses for each rule, useful for making internal services accessible externally.

## Important Files

- `device.py`: Defines the `Device` class to store individual device information.
- `device_manager.py`: Handles device parsing and unification from DHCP and connected devices list.
- `dhcp_config.py`: Manages DHCP configuration settings and requests.
- `dyndns_config.py`: Manages DynDNS configuration and updates.
- `port_forwarding.py`: Handles port forwarding configuration.
- `modem_client.py`: Connects to the modem, handles authentication, and sends requests.
- `install_requirements.py`: Installs required Python packages.

## Notes

- Ensure you have the correct credentials to access your modem.
- This tool is designed specifically for Technicolor TIM modems and may not be compatible with other models.
