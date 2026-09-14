# 1. Load your threat intelligence database
with open("blacklist.txt", "r") as file:
    threat_feed = [line.strip() for line in file.readlines()]

# 2. Read your incoming traffic network log
with open("auth_log.txt", "r") as file:
    log_lines = file.readlines()


print("=== AUDOMATED SIEM CORRLATION REPORT ===")

for line in log_lines:
    line = line.strip()
    
    # Extract the IP address from the log line
    if "IP:" in line:
        parts = line.split(" - ")
        ip_part = parts[1] # Grab the "IP:xxx" segment
        ip_address = ip_part.replace("IP:", "")
        
        if ip_address in threat_feed:
            print(f"[ CRITICAL CORRELATION ] Attacker IP {ip_address} identified in system traffic log!")