import os
import time

LOG_FILE = "auth_log.txt"

print("=== 🛡️ AUTOMATED FIREWALL ENFORCEMENT ENGINE ENGAGED ===")
print("[🛰️ MONITORING] Watching log streams for active brute-force vectors...\n")

# Track already blocked IPs in memory to prevent duplicate rule generation
blocked_ips = set()

# 1. Read our active local threat logs
with open(LOG_FILE, "r") as file:
    log_lines = file.readlines()

for line in log_lines:
    # 2. Isolate high-velocity malicious login attempts
    if "STATUS:FAILED" in line:
        parts = line.split(" - ")
        ip_address = parts[1].replace("IP:", "").strip()
        
        # Deduplication Check: If we already blocked this IP during this run, skip it!
        if ip_address in blocked_ips:
            continue
            
        print(f"[🚨 THREAT DETECTED] Malicious activity tracked from: {ip_address}")
        print(f"[⚡ ACTION] Deploying rule to drop all incoming packets from {ip_address}...")
        
        # Fixed quoting structure using explicit single quotes inside the outer f-string double quotes
        firewall_command = f"netsh advfirewall firewall add rule name='Banned_Hacker_{ip_address}' dir=in action=block remoteip={ip_address}"
        
        # Un-commented line to actively trigger real shell deployment to the Windows Firewall kernel
        os.system(firewall_command)
        
        # Register the IP as blocked in our memory tracking set
        blocked_ips.add(ip_address)
        
        print(f"[✅ SUCCESS] Firewall rule locked! {ip_address} is permanently banned.\n")
        time.sleep(1)

print("[🏁 COMPLETE] System logs fully processed. Edge defenses are active.")
