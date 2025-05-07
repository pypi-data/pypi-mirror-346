import sqlite3  # SQLite library for lightweight local database operations

def insert_known_host(mac, ip=None, hostname=None, vendor=None, os=None, notes=None):
    """
    Inserts or updates a known device into the 'known_hosts' database.

    Parameters:
        mac (str): MAC address (primary key)
        ip (str, optional): IP address of the device
        hostname (str, optional): Hostname of the device
        vendor (str, optional): MAC vendor or manufacturer
        os (str, optional): Operating system information
        notes (str, optional): Any additional notes
    """

    # Connect to the local SQLite database file (creates it if it doesn't exist)
    conn = sqlite3.connect("known_hosts.db")
    c = conn.cursor()

    # Create the 'known_hosts' table if it doesn't already exist
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

    # Insert a new row or update existing row (matched by MAC address)
    # Uses "ON CONFLICT" to update the existing row instead of inserting a duplicate
    c.execute('''
        INSERT INTO known_hosts (mac, ip, hostname, vendor, os, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(mac) DO UPDATE SET
            ip=excluded.ip,
            hostname=excluded.hostname,
            vendor=excluded.vendor,
            os=excluded.os,
            notes=excluded.notes
    ''', (mac, ip, hostname, vendor, os, notes))

    # Save changes and close the connection
    conn.commit()
    conn.close()

    # Confirmation output
    print(f"[✓] Saved: {mac}")

# Example usage when running this script directly
if __name__ == "__main__":
    insert_known_host(
        "AA:BB:CC:DD:EE:FF",
        ip="192.168.1.100",
        hostname="MyDevice",
        vendor="Cisco",
        os="Linux",
        notes="Lab test device"
    )
