import json

def analyze_logs(log_file):
    """Analyze honeypot logs for repeated IPs and commands."""
    ip_counts = {}
    command_counts = {}

    with open(log_file, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                ip = entry['client_ip']
                data = entry['data']

                # Count IP occurrences
                ip_counts[ip] = ip_counts.get(ip, 0) + 1

                # Count commands if present
                if 'command' in data:
                    cmd = data['command']
                    command_counts[cmd] = command_counts.get(cmd, 0) + 1

            except json.JSONDecodeError:
                continue

    # Print results
    print("IP Frequency:")
    for ip, count in ip_counts.items():
        print(f"  {ip}: {count} connections")

    print("\nCommand Frequency:")
    for cmd, count in command_counts.items():
        print(f"  {cmd}: {count} attempts")

if __name__ == "__main__":
    log_file = "logs/honeypot.log"
    analyze_logs(log_file)
