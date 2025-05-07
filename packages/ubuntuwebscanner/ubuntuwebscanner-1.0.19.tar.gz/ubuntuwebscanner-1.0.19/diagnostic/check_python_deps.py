import importlib
import os
import platform

def check_python_packages(requirements_path='requirements.txt'):
    """Check if all required Python packages listed in requirements.txt are installed."""

    print("\n📦 Python Dependencies Check:")

    # Detect and display the OS platform
    current_os = platform.system()
    print(f"🖥️ Detected OS: {current_os}")

    if not os.path.exists(requirements_path):
        print("❌ requirements.txt not found.")
        return

    # Read and check each package from requirements.txt
    with open(requirements_path) as f:
        for line in f:
            # Skip comments and empty lines
            if not line.strip() or line.startswith('#'):
                continue

            # Extract package name before '=='
            pkg = line.split('==')[0].strip()

            try:
                # Try importing using Python module naming conventions
                importlib.import_module(pkg.replace('-', '_'))
                print(f"{pkg}: ✓ found")
            except ImportError:
                print(f"{pkg}: ✗ MISSING")

    print("\n✅ Package check complete.\n")

if __name__ == "__main__":
    check_python_packages()
