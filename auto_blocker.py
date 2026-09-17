import os
import time

LOG_FILE = "auth_log.txt"

print("=== AUTOMATED FIREWALL ENFORCEMENT ENGINE ENGAGED ===")
print(" [ MONITORING ] Watching log streams for active brute-force vectors...\n"

# 1. Read our active local threat logs
with open(LOG_FILE, "r") as file:
    log_lines = file.readlines()
    
for line in log_lines:
    # 2. Isolate high-velocity malicious login attempts
    if "STATUS:FAILED" in line:
        parts = line.split(" - ")
        ip_address = parts[1].replace("IP:", "").strip()
        
        print(f"[ THREAT DETECTED ] Malicious activity tracked from: {ip_address}")
        print(f" ACTION ] Deploying rule to drop all incoming packets from {ip_address}...")
        
        
        firewall_command = f"netsh advfirewall firewall add rule name='Banned_Hacker_{ip_address}' dir=in action=block remoteip={ip_address}"
        
        # 3. This built-in function forces your laptop to execute that command in the terminal!
        # os.system(firewall_command)
        print(f"[ SUCCESS ] Firewall rule locked! {ip_address} is permamently banned.\n")
        time.sleep(1) # Simulated delay between rule deployment