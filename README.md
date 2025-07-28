Python-based SSH honeypot to log, analyze, and block attackers with geolocation visualization.

````markdown
# SSH Honeypot

A simple Python-based SSH honeypot designed to simulate a vulnerable SSH service, capture unauthorized access attempts, analyze attacker behavior, and visualize geographic attack sources. This project is intended for educational and research purposes.

---

## Features

- SSH honeypot listening on port 2222
- Logs IP addresses, usernames, passwords, and commands
- Detects and analyzes repeated login attempts
- Fail2Ban integration to block malicious IPs
- Generates a geolocation plot of attacker IPs
- Tested between Ubuntu (host) and Kali Linux (attacker)

---

## Requirements

- Python 3.x
- pip
- fail2ban
- UFW (optional, for firewall rules)
- DB-IP City Lite database for geolocation

---

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/HoneyPot-Project.git
   cd HoneyPot-Project
````

2. **Install dependencies:**

   ```bash
   pip3 install geoip2 matplotlib
   sudo apt update && sudo apt install fail2ban -y
   ```

3. **Download and extract the geolocation database:**

   * Register and download from: [https://db-ip.com/db/](https://db-ip.com/db/)
   * Move and extract the file:

     ```bash
     mkdir geoip
     mv dbip-city-lite-2025-07.mmdb.gz geoip/
     gunzip geoip/dbip-city-lite-2025-07.mmdb.gz
     ```

---

## Configuration

Create the following file at `config/honeypot_config.json`:

```json
{
  "port": 2222,
  "log_path": "logs/honeypot.log",
  "banner": "SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3"
}
```

For Fail2Ban integration:

* Copy `fail2ban/jail.local` and `fail2ban/filter.d/honeypot.conf` to `/etc/fail2ban/`.

---

## Usage

### On the Honeypot Server (Ubuntu)

1. Allow port 2222:

   ```bash
   sudo ufw allow 2222
   ```

2. Start the honeypot:

   ```bash
   cd scripts
   python3 ssh_honeypot.py
   ```

3. Check your local IP address:

   ```bash
   ip addr
   ```

### On the Attacker Machine (Kali Linux)

1. Install telnet:

   ```bash
   sudo apt update && sudo apt install telnet -y
   ```

2. Connect to the honeypot:

   ```bash
   telnet <Ubuntu-IP> 2222
   ```

3. Simulate an attack:

   ```
   user root
   pass 123456
   whoami
   ```

   Repeat several times to trigger a ban.

---

## Verifying the Setup

* Check logs:

  ```bash
  cat logs/honeypot.log
  ```

* Check Fail2Ban status:

  ```bash
  sudo fail2ban-client status honeypot-ssh
  ```

* Generate geolocation plot:

  ```bash
  cd scripts
  python3 geo_visualizer.py
  ```

  Output: `reports/ip_geolocation.png`

---

## Directory Structure

```
python-honeypot/
├── scripts/
│   ├── ssh_honeypot.py
│   ├── log_analyzer.py
│   └── geo_visualizer.py
├── config/
│   └── honeypot_config.json
├── geoip/
│   └── dbip-city-lite.mmdb
├── logs/
│   └── honeypot.log
├── reports/
│   └── ip_geolocation.png
```

---

## Future Work

* Email alerts for banned IPs
* Heatmap support in geolocation output
* Dockerize the project for easier deployment
