from flask import Flask, render_template
import nmap                           # Python wrapper for Nmap
from manuf import manuf               # Library to detect MAC vendors
import os
import json
from ubuntuwebserver import config    # Custom config module (ensure TEST_MODE flag)
import psutil                         # Interface stats and addresses
import ipaddress                      # Clean subnet calculations

# Flask web application setup
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# Parser to identify hardware vendors from MAC addresses
mac_parser = manuf.MacParser()

# Return all active network interfaces (except loopback)
def get_active_interfaces():
    return [iface for iface, stats in psutil.net_if_stats().items()
            if stats.isup and not iface.startswith('lo')]

# Scan the local network using Nmap and return device metadata
def scan_network():
    # Optional mock mode for dev/testing without live scan
    if config.TEST_MODE:
        print("[TEST MODE] Returning mock scan results.")
        return [{
            'ip': '192.168.1.10',
            'hostname': 'MockHost',
            'mac': 'AA:BB:CC:DD:EE:FF',
            'vendor': 'MockVendor',
            'os': 'MockOS',
            'notes': 'Test device'
        }]

    # Load cached OS info (if available)
    def load_os_cache():
        try:
            with open("/tmp/os_cache.json") as f:
                return json.load(f).get("os_results", {})
        except Exception:
            return {}

    os_cache = load_os_cache()
    nm = nmap.PortScanner()
    hosts = []

    # Iterate through all active interfaces
    for iface in get_active_interfaces():
        addrs = psutil.net_if_addrs().get(iface, [])

        for addr in addrs:
            if addr.family.name == 'AF_INET':  # IPv4 only
                ip = addr.address
                netmask = addr.netmask

                if ip and netmask:
                    try:
                        # Convert IP/netmask to full subnet range
                        subnet = str(ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False))
                        print(f"[INFO] Scanning {subnet} on interface: {iface}")

                        # Use `-e` (interface flag) on Linux/Mac only; not supported on Windows
                        if os.name == 'nt':  # Windows
                            nm.scan(hosts=subnet, arguments="-sn")
                        else:
                            nm.scan(hosts=subnet, arguments=f"-sn -e {iface}")

                        print(f"[DEBUG] Found hosts on {subnet}: {nm.all_hosts()}")

                        # Parse results
                        for host in nm.all_hosts():
                            try:
                                mac = nm[host]['addresses'].get('mac', 'N/A')
                                vendor = mac_parser.get_manuf(mac) if mac != "N/A" else "N/A"
                                os_info = os_cache.get(host, "Unknown")
                                hostname = nm[host].hostname()

                                print(f"[DEBUG] Added host: IP={host}, Hostname={hostname}, MAC={mac}, Vendor={vendor}, OS={os_info}")

                                hosts.append({
                                    'ip': host,
                                    'hostname': hostname,
                                    'mac': mac,
                                    'vendor': vendor,
                                    'os': os_info
                                })

                            except Exception as e:
                                print(f"[WARNING] Failed to parse host {host}: {e}")

                    except Exception as e:
                        print(f"[ERROR] Failed scanning subnet {subnet} on iface {iface}: {e}")

    return hosts

# Flask route for root webpage
@app.route("/")
def home():
    results = scan_network()
    print(f"[INFO] Returning {len(results)} scan results to UI.")
    return render_template("scan_results.html", results=results)

# Entrypoint for running Flask directly (used when not running through WSGI server)
def main():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# Run app if this script is launched directly
if __name__ == "__main__":
    main()
