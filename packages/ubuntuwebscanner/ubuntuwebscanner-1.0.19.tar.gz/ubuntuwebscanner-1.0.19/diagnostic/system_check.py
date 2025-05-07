#!/usr/bin/env python3

import shutil
import psutil
import os
import platform
import subprocess

def check_command(cmd):
    """Check if a command is available in system PATH."""
    return shutil.which(cmd) is not None

def show_ip_config():
    """Display IP configuration based on the operating system."""
    system = platform.system()
    print("\n🖧 IP Configuration:")
    if system == "Linux":
        # Prefer `ip a`, fallback to `ifconfig`
        os.system("ip a" if check_command("ip") else "ifconfig")
    elif system == "Windows":
        os.system("ipconfig")
    elif system == "Darwin":  # macOS
        os.system("ifconfig")
    else:
        print("Unknown OS. Cannot determine network configuration command.")

def main():
    print("=== 🌐 UbuntuWebScanner Diagnostic Tool ===\n")

    # System Information
    print(f"🔧 Python Version: {platform.python_version()}")
    print(f"🖥️ Operating System: {platform.system()} {platform.release()}\n")

    # CLI Tool Dependency Check
    print("📦 Required Command-Line Tools:")
    for tool in ['nmap', 'sqlite3', 'curl', 'ping']:
        status = '✓ found' if check_command(tool) else '✗ missing'
        print(f"  - {tool}: {status}")

    # Network Configuration
    show_ip_config()

    # System Resource Usage
    print("\n🧠 System Resource Usage:")
    print(f"  - CPU Usage: {psutil.cpu_percent()}%")
    print(f"  - Memory Usage: {psutil.virtual_memory().percent}%")
    print(f"  - Disk Usage: {psutil.disk_usage('/').percent}%")

    print("\n✅ Diagnostic Complete.\n")

if __name__ == '__main__':
    main()
