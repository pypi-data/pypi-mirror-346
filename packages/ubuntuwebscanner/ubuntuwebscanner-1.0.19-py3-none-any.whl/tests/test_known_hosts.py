# test_known_hosts.py
#
# MIT License
# (c) 2025 Timothy Johnson II
#
# This test suite validates the behavior of the `get_known_host_info()` function,
# ensuring it correctly retrieves known hosts from the database and handles unknown ones properly.

import unittest
import sqlite3
from ubuntuwebserver.app import get_known_host_info

class TestKnownHosts(unittest.TestCase):
    def setUp(self):
        """
        This method is run before each test.
        It sets up a temporary in-memory SQLite database and inserts a test record.
        It also monkey-patches the database connection used by the target function
        so it uses this test DB instead of a real file.
        """
        self.conn = sqlite3.connect(':memory:')  # Create a temporary in-memory DB
        self.cursor = self.conn.cursor()

        # Create the table structure
        self.cursor.execute('''
            CREATE TABLE known_hosts (
                mac TEXT PRIMARY KEY,
                ip TEXT,
                hostname TEXT,
                vendor TEXT,
                os TEXT,
                notes TEXT
            )
        ''')

        # Insert a test host record
        self.cursor.execute('''
            INSERT INTO known_hosts (mac, ip, hostname, vendor, os, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            'AA:BB:CC:DD:EE:FF',
            '192.168.1.100',
            'TestHost',
            'TestVendor',
            'TestOS',
            'This is a test entry'
        ))
        self.conn.commit()

        # Monkey patch the sqlite3.connect function used in the app module
        # This ensures the tested function uses our in-memory DB
        import ubuntuwebserver.app as app
        app.get_known_host_info.__globals__['sqlite3'].connect = lambda _: self.conn

    def tearDown(self):
        """
        This method runs after each test.
        It closes the in-memory database connection.
        """
        self.conn.close()

    def test_known_host_lookup(self):
        """
        Test that a known MAC address returns the correct metadata.
        """
        result = get_known_host_info('AA:BB:CC:DD:EE:FF')
        self.assertIsNotNone(result)
        self.assertEqual(result['hostname'], 'TestHost')
        self.assertEqual(result['vendor'], 'TestVendor')
        self.assertEqual(result['os'], 'TestOS')
        self.assertEqual(result['notes'], 'This is a test entry')

    def test_unknown_host_lookup(self):
        """
        Test that an unknown MAC address returns None.
        """
        result = get_known_host_info('00:11:22:33:44:55')
        self.assertIsNone(result)

# Run the test suite
if __name__ == '__main__':
    unittest.main()
