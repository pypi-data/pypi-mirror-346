# MIT License
# 
# Copyright (c) 2025 Timothy Johnson II
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
from ubuntuwebserver.app import scan_network

class TestScanner(unittest.TestCase):
    """
    Unit test class for the scan_network function in the ubuntuwebserver.app module.
    """

    def test_scan_not_empty(self):
        """
        This test runs scan_network in test mode (which returns mock data),
        and asserts that the returned result is a non-empty list.
        """
        results = scan_network(test_mode=True)  # Inject test mode to avoid real network scanning
        self.assertIsInstance(results, list)     # Ensure the return type is a list
        self.assertGreater(len(results), 0)      # Ensure the list is not empty

if __name__ == '__main__':
    # Executes the test if this file is run directly
    unittest.main()
