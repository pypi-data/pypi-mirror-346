=======================================================================
🌐 UbuntuWebServer - Flask Network Scanner
=======================================================================

A modern, lightweight network device scanner built with Flask and Python.
Detects all devices on your local network (IP, MAC, hostname, vendor, OS)
and provides a clean, auto-refreshing web UI. Optional cron-based deep scans
and tagging/notes for known hosts.

-----------------------------------------------------------------------
✅ PROJECT GOAL
-----------------------------------------------------------------------

Create a web-based dashboard that:
- Scans LAN for connected devices (IP, MAC, Hostname, Vendor, OS)
- Stores and displays known devices in a SQLite database
- Provides an editable UI for tagging/notes
- Supports automated OS scanning and refresh via cron
- Can run persistently with systemd or a background process

-----------------------------------------------------------------------
🛠 TOOLS & TECHNOLOGIES
-----------------------------------------------------------------------

Task                    | Tool
------------------------|-------------------------------
Web Server              | Flask (Apache2 optional)
Backend                 | Python 3.10+
Network Scanning        | nmap, mac-vendor-lookup
Frontend UI             | HTML/CSS, Bootstrap
Database Storage        | SQLite
Scheduling              | cron (Linux/macOS)
Startup Service         | systemd (Linux)

-----------------------------------------------------------------------
🧱 ARCHITECTURE OVERVIEW
-----------------------------------------------------------------------

[ Ubuntu Server / Windows / Mac ]
          |
     [ Flask App - app.py ]
          |
[ nmap scan → parsed into DB ]
          |
[ SQLite + MAC Vendor DB ]
          |
[ Auto-refresh Web UI /cron ]

-----------------------------------------------------------------------
🧪 INSTALLATION INSTRUCTIONS
-----------------------------------------------------------------------

1. Clone and Set Up Environment
-------------------------------
git clone https://github.com/tjohnsonII/UbuntuWebServer.git
cd UbuntuWebServer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Install System Dependencies (Linux/macOS)
--------------------------------------------
sudo apt update
sudo apt install nmap sqlite3 -y

3. Initialize the Database
--------------------------
bash init_db.sh

4. Run the Web App
------------------
bash run_flask.sh

Then open in browser:
http://<server-ip>:5000

-----------------------------------------------------------------------
🔁 GITHUB SYNC & AUTO RESTART
-----------------------------------------------------------------------

To sync latest updates from GitHub and restart Flask:
bash sync_from_github.sh

-----------------------------------------------------------------------
🔂 AUTOMATE DEEP OS SCANNING
-----------------------------------------------------------------------

To install cron job that scans every 30 minutes:
bash install_cron.sh

This creates:
*/30 * * * * /usr/bin/python3 /home/<user>/UbuntuWebServer/deep_scan.py

-----------------------------------------------------------------------
🚀 ENABLE ON BOOT (systemd)
-----------------------------------------------------------------------

sudo cp flaskscanner.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable flaskscanner
sudo systemctl start flaskscanner

-----------------------------------------------------------------------
🧾 ADD / EDIT KNOWN HOSTS
-----------------------------------------------------------------------

Run this to insert devices with notes:
python insert_known_host.py

Prompts for:
- MAC
- IP
- Hostname
- Vendor
- OS
- Notes

-----------------------------------------------------------------------
📂 PROJECT LAYOUT
-----------------------------------------------------------------------

File/Folder               | Purpose
--------------------------|------------------------------------------
ubuntuwebserver/app.py    | Flask scanner logic
deep_scan.py              | OS detection w/ cron
insert_known_host.py      | CLI insert known devices
init_db.py                | SQLite DB init
templates/scan_results.html | Auto-refresh UI
known_hosts.db            | Local device info
sync_to_github.sh         | Push latest code
sync_from_github.sh       | Pull + restart
run_flask.sh              | Run web server
start-networkscanner.sh   | Smart launch script
flask.log / app_errors.log| Logging

-----------------------------------------------------------------------
🌐 WEB UI FEATURES
-----------------------------------------------------------------------

- Auto-refresh every 15 seconds
- Search/filter by IP, MAC, hostname, vendor
- Bootstrap responsive design
- Color-coded vendor badges
- OS detection support
- Notes/comments per device

-----------------------------------------------------------------------
🛠 CROSS-PLATFORM NOTES
-----------------------------------------------------------------------

✔ Linux        - Full support (cron, systemd, bash)
✔ macOS        - Supported with `brew install nmap sqlite3`
✔ Windows      - Use Git Bash or WSL + Python 3.10+
               - Adjust paths in bash scripts as needed
               - Flask auto-refresh supported

-----------------------------------------------------------------------
🩺 TROUBLESHOOTING
-----------------------------------------------------------------------

- Port 5000 busy? Run: `lsof -i :5000` or `sudo fuser -k 5000/tcp`
- nmap not found? Run: `sudo apt install nmap`
- Python error? Verify Python 3.10+ and correct venv
- No output? Check scan logs in flask.log or run `scanScript.py`

-----------------------------------------------------------------------
⚠️ SECURITY WARNING
-----------------------------------------------------------------------

This tool is for **private/internal LANs only**.
Do NOT expose to the public internet.
There is no built-in authentication or encryption.
Use firewalls, VPN, or nginx basic auth if needed.

-----------------------------------------------------------------------
📄 LICENSE
-----------------------------------------------------------------------

MIT License © 2025 Timothy Johnson II

-----------------------------------------------------------------------
🙋 AUTHOR
-----------------------------------------------------------------------

Timothy Johnson II
Hosted PBX Engineer, 123NET
GitHub: https://github.com/tjohnsonII
