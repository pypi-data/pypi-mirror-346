import psutil
import ipaddress

# Function to detect and compute the local IPv4 subnet
def get_local_subnet():
    for iface_name, iface_addrs in psutil.net_if_addrs().items():
        for addr in iface_addrs:
            # Only consider active IPv4 addresses on non-loopback interfaces
            if addr.family.name == 'AF_INET' and not iface_name.startswith("lo"):
                ip = addr.address
                netmask = addr.netmask
                if ip and netmask:
                    try:
                        # Combine IP address and netmask to determine subnet
                        network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                        print(f"[INFO] Computed local subnet: {network}")
                        return str(network)
                    except Exception as e:
                        print(f"[ERROR] Failed to calculate subnet: {e}")
    # Fallback to loopback subnet if no valid interface found
    return "127.0.0.1/32"

# -------------------
# Static Configuration
# -------------------

# Optional: Manually define a fallback/default subnet for scanning
NETWORK_RANGE = "192.168.1.0/24"

# SQLite database path to store known host data
DATABASE_PATH = "known_hosts.db"

# Log file for general Flask application logs
LOG_FILE = "flask.log"

# Log file for catching app-level errors
ERROR_LOG_FILE = "app_errors.log"

# Dynamically determined subnet for actual scanning (overrides NETWORK_RANGE if used)
SUBNET = get_local_subnet()

# Interval in minutes to run automatic scans (if scheduled)
SCAN_INTERVAL = 30  # in minutes

# Enable verbose Flask logging and exception details
DEBUG_MODE = False

# Enable mock scan results for testing UI without running Nmap
TEST_MODE = False
