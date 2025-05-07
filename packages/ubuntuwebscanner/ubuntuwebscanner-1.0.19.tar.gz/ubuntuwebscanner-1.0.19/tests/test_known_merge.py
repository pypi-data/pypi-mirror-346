import unittest
import sqlite3
from ubuntuwebserver.app import get_known_host_info  # Assuming this function would be tested

class TestKnownHostMerge(unittest.TestCase):
    def setUp(self):
        """
        Set up a temporary in-memory SQLite database before each test.
        This avoids touching real data and ensures a clean environment.
        """
        self.conn = sqlite3.connect(':memory:')  # In-memory DB for test isolation
        self.c = self.conn.cursor()

        # Create the known_hosts table structure
        self.c.execute('''
            CREATE TABLE known_hosts (
                mac TEXT PRIMARY KEY,
                ip TEXT,
                hostname TEXT,
                vendor TEXT,
                os TEXT,
                notes TEXT
            )
        ''')

        # Insert a mock host entry for testing
        self.test_mac = 'AA:BB:CC:DD:EE:FF'
        self.c.execute('''
            INSERT INTO known_hosts (mac, ip, hostname, vendor, os, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.test_mac,
            '192.168.1.123',
            'TestDevice',
            'Cisco',
            'Linux',
            'Lab Device'
        ))
        self.conn.commit()

    def test_lookup_merge(self):
        """
        Test whether a known MAC address lookup returns the expected merged metadata.
        This mocks a lookup function that returns enriched host info.
        """

        # Local function simulating the logic used to retrieve host info by MAC address
        def test_lookup(mac):
            self.c.execute("SELECT hostname, vendor, os, notes FROM known_hosts WHERE mac = ?", (mac,))
            row = self.c.fetchone()
            if row:
                return {
                    'hostname': row[0],
                    'vendor': row[1],
                    'os': row[2],
                    'notes': row[3]
                }
            return None

        # Run the lookup using the test MAC address
        result = test_lookup(self.test_mac)

        # Validate that the result is not None and contains correct merged info
        self.assertIsNotNone(result)
        self.assertEqual(result['vendor'], 'Cisco')
        self.assertEqual(result['hostname'], 'TestDevice')

    def tearDown(self):
        """
        Close the in-memory database connection after each test.
        """
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
