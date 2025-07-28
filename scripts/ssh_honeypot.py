import socket
import threading
import json
import time
import os
from datetime import datetime

# Load configuration
with open('../config/honeypot_config.json', 'r') as f:
    config = json.load(f)

PORT = config['port']
LOG_PATH = config['log_path']
BANNER = config['banner']

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def log_interaction(ip, data):
    """Log client interaction to a file in JSON format."""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'client_ip': ip,
        'data': data
    }
    with open(LOG_PATH, 'a') as f:
        json.dump(log_entry, f)
        f.write('\n')

def handle_client(client_socket, client_address):
    """Handle a single client connection."""
    try:
        # Send SSH banner
        client_socket.send(f"{BANNER}\r\n".encode())
        log_interaction(client_address[0], {"banner_sent": BANNER})

        # Prompt for username
        client_socket.send(b"login: ")
        username = client_socket.recv(1024).decode().strip()
        log_interaction(client_address[0], {"username": username})

        # Prompt for password
        client_socket.send(b"password: ")
        password = client_socket.recv(1024).decode().strip()
        log_interaction(client_address[0], {"password": password})

        # Fake shell prompt
        client_socket.send(b"$ ")
        command = client_socket.recv(1024).decode().strip()
        log_interaction(client_address[0], {"command": command})

        # Simulate command response
        if command:
            client_socket.send(b"command not found\r\n$ ")
        else:
            client_socket.send(b"$ ")

    except Exception as e:
        log_interaction(client_address[0], {"error": str(e)})
    finally:
        client_socket.close()

def main():
    """Run the honeypot server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', PORT))
    server.listen(5)
    print(f"Honeypot listening on port {PORT}...")

    while True:
        client_socket, client_address = server.accept()
        log_interaction(client_address[0], {"connection": "established"})
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()
