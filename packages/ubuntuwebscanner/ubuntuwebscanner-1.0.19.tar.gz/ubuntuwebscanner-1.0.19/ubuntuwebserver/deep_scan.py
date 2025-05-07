import sqlite3        # Used for interacting with the SQLite database
import nmap           # Python wrapper for running and parsing Nmap scans
from datetime import datetime  # For timestamping scan start

# ----------------------------
# Database Update Function
# ----------------------------

def update_os_in_db(ip, mac, os_info):
    """
    Insert or update the OS information for a known device into the SQLite database.
    If the MAC address already exists, the OS value is updated.
    """
    conn = sqlite3.connect("known_hosts.db")
    c = conn.cursor()

    # Ensure the table exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS known_hosts (
            mac TEXT PRIMARY KEY,
            ip TEXT,
            hostname TEXT,
            vendor TEXT,
            os TEXT,
            notes TEXT
        )
    ''')

    # Insert new or update existing entry using UPSERT logic
    c.execute('''
        INSERT INTO known_hosts (mac, ip, os)
        VALUES (?, ?, ?)
        ON CONFLICT(mac) DO UPDATE SET os=excluded.os
    ''', (mac, ip, os_info))

    conn.commit()
    conn.close()

# ----------------------------
# Deep OS Detection Scan
# ----------------------------

def deep_scan():
    """
    Perform an Nmap OS detection scan on the local subnet and update the database
    with any detected operating system info.
    """
    nm = nmap.PortScanner()

    # Run an OS detection scan across the 192.168.1.0/24 network
    nm.scan(hosts='192.168.1.0/24', arguments='-O')  # '-O' enables OS detection

    for host in nm.all_hosts():
        ip = host  # IP address of the detected host
        mac = nm[host]['addresses'].get('mac', 'N/A')  # Try to extract MAC address
        os_info = "N/A"

        # If OS matches are returned, use the first/best match
        if 'osmatch' in nm[host] and nm[host]['osmatch']:
            os_info = nm[host]['osmatch'][0]['name']

        # Only update database if MAC address is available (used as primary key)
        if mac != "N/A":
            update_os_in_db(ip, mac, os_info)
            print(f"[✓] {ip} ({mac}) -> {os_info}")

# ----------------------------
# Script Entry Point
# ----------------------------

if __name__ == "__main__":
    # Log when the scan starts
    print(f"Started deep scan at {datetime.now()}")
    deep_scan()
