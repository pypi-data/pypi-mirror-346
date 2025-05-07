# Import necessary tools from unittest.mock to simulate dependencies
from unittest.mock import MagicMock, patch
import ubuntuwebserver.app as app  # Ensure the path to your app.py is correct relative to this test file

# Patch the nmap.PortScanner class in the app module to prevent actual network scans
@patch('app.nmap.PortScanner')
def test_scan_mocked(scanner_mock):
    """
    This test mocks the nmap.PortScanner to simulate a scan_network() call.
    It verifies the return structure when a single fake device is scanned.
    """

    # Create a fake scanner instance that the patch will use
    scanner_instance = scanner_mock.return_value

    # Simulate scan behavior: .scan() does nothing
    scanner_instance.scan.return_value = None

    # Simulate that one host was "found"
    scanner_instance.all_hosts.return_value = ['192.168.1.10']

    # Simulate host information returned by the mock scanner
    scanner_instance.__getitem__.return_value = {
        'addresses': {'mac': 'AA:BB:CC:DD:EE:FF'},
        'hostname': lambda: 'MockHost'  # Emulate the .hostname() method
    }

    # Run the network scan in test mode (bypasses real scan logic)
    results = app.scan_network(test_mode=True)

    # Validate that the output is a list and has the expected content
    assert isinstance(results, list)
    assert results[0]['ip'] == '192.168.1.10'
    assert results[0]['mac'] == 'AA:BB:CC:DD:EE:FF'
