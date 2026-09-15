import urllib.request
import json
import csv

# 1. External Data Sources
THREAT_URL = "https://api.tweetfeed.live/v1/blocklist/ips.txt"
GEO_API = "http://ip-api.com"

print(" [STARTING] Ingesting live global threat database...")

#Fetch threat list with browser headers
try:
    req = urllib.request.Request(THREAT_URL)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    with urllib.request.urlopen(req) as response:
        threat_feed = [ip.strip() for ip in response.read().decode('utf-8').splitlines()]
    print(f"[SUCCESS] Downloaded {len(threat_feed)} active hacker IPs from the web!")
except Exception as e:
    print(f"[ ERROR] Threat feed download failed: {e}")
    threat_feed = []

#Injecting out test IP to ensure it tests the parsing architechture successfully
#   threat_feed.append("203.0.113.42")
 #   print(threat_feed)

# 2. Open our Local spreadsheet file to save catches
with open("threat_report.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # Write the spreadsheet headers
    writer.writerow(["Timestamp", "Attacker IP", "Geographic Country", "Risk Level"])
    
    # 3. Scan Local system Log metrics
    with open("auth_log.txt", "r") as log_file:
        for line in log_file:
            if "STATUS:FAILED" in line:
                parts = line.split(" - ")
                timestamp = parts[0]
                ip_address = parts[1].replace("IP:", "").strip() # <-- Added .strip() here to remove space if any
                
                # 4. Perform the live lookups
                if ip_address in threat_feed:
                    # Fetch Country via GeoIP API
                    try:
                        with urllib.request.urlopen(GEO_API + ip_address) as geo_res:
                            geo_data = json.loads(geo_res.read().decode('utf-8'))
                            country = geo_data.get("country", "Unknown Location")
                    except:
                        country = "Lookup Failed"
                     
                    print(f"[ CORRELATION] Caught threat from {ip_address} ({country})")
                    
                    writer.writerow([timestamp, ip_address, country, "CRITICAL"])
                    
print(" [ COMPLETE] Audit finished. threat_report.csv has been successfully compiled.")