import nmap  # Import the Nmap wrapper for Python

# Initialize the Nmap PortScanner object
nm = nmap.PortScanner()

# Perform a simple "ping scan" to detect live hosts in the given subnet
# -sn = No port scan; just check which hosts are up (ping scan)
nm.scan(hosts='192.168.1.0/24', arguments='-sn')

# Iterate over all detected (alive) hosts
for host in nm.all_hosts():
    # Retrieve the hostname (if available) and MAC address (if provided)
    hostname = nm[host].hostname()
    mac_address = nm[host]['addresses'].get('mac', 'N/A')

    # Print the IP, hostname, and MAC address of each discovered host
    print(f"Host: {host} ({hostname}) | MAC: {mac_address}")
