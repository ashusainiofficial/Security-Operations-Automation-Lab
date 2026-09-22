import urllib.request

# 1. Direct URL to a real, live open-source IP threat blocklist feed
FEED_URL = "https://tweetfeed.live"

print(" [CONNECTING ] Fetching live hacker IP database from threatfeed...")

try:
    # Connect to the internet link and download the data tect
    #1. Create a request objectand explicitly inject a standard browser User-Agent header
    req = urllib.request.Request(FEED_URL)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    
    #2. pass your customized request object into the urlopen engine
    with urllib.request.urlopen(req) as response:
        raw_data = response.read().decode('utf-8')
        
    # Split the massive text stream into a tructured python list of IPs
    live_threat_feed = [ip.strip() for ip in raw_data.splitlines() if ip.strip()]
    print(f"[ SUCCESS ] Downloaded {len(live_threat_feed)} active hacker IPs from the web!")

except Exception as e:
    print(f"[ ERROR ] Network connection failed: {e}")
    live_threat_feed = []

# 2. Open your local corporate sandbox traffic log
with open("auth_log.txt", "r") as file:
    log_lines = file.readlines()

print("\n=== LIVE SIEM CORRELATION REPORT ===")
for line in log_lines:
    line = line.strip()
    
    if "IP:" in line:
        parts = line.split(" - ")
        ip_part = parts[1]
        ip_address = ip_part.replace("IP:", "")
        
        
        if ip_address in live_threat_feed:
            print(f"[ CRITICAL INTERCEPT ] Dynamic match! Malicious IP {ip_address} found in traffic logs!")