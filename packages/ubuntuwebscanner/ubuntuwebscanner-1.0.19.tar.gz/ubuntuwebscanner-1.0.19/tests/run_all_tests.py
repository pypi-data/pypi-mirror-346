import unittest

# Entry point for the test runner script
if __name__ == '__main__':
    # Create a test loader instance to search for test cases
    loader = unittest.TestLoader()
    
    # Discover and load all test files in the 'tests' directory
    # Files must be named like 'test*.py' (default pattern)
    suite = loader.discover('tests')

    # Create a test runner that outputs results with verbosity level 2 (more detailed)
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the entire discovered test suite
    runner.run(suite)
