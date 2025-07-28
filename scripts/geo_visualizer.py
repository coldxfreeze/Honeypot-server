import json
import os
import geoip2.database
import matplotlib.pyplot as plt

# Set up GeoIP database
geo_db_path = '/home/coldxfreeze/Desktop/project/python-honeypot/geoip/dbip-city-lite-2025-07.mmdb'
reader = geoip2.database.Reader(geo_db_path)

# Read honeypot logs
log_file = '/home/coldxfreeze/Desktop/project/python-honeypot/logs/honeypot.log'
if not os.path.exists(log_file):
    print("No log file found at {log_file}. Run the honeypot first!")
    exit(1)

# Collect IP locations
locations = {}
with open(log_file, 'r') as f:
    for line in f:
        try:
            entry = json.loads(line.strip())
            ip = entry['client_ip']
            try:
                response = reader.city(ip)
                lat = response.location.latitude
                lon = response.location.longitude
                locations[ip] = (lat, lon)
            except geoip2.errors.AddressNotFoundError:
                locations[ip] = (None, None)  # Unknown location
        except json.JSONDecodeError:
            print("Skipping a bad log entry...")

# Plotting
plt.figure(figsize=(10, 6))
for ip, (lat, lon) in locations.items():
    if lat and lon:
        plt.plot(lon, lat, 'bo', label=ip if ip not in plt.gca().get_legend_handles_labels()[1] else "")
plt.title('Attacker Geolocation')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.legend(title='IP Addresses')
plt.savefig('../reports/ip_geolocation.png')
plt.close()

reader.close()
print("Geolocation plot saved as reports/ip_geolocation.png")
