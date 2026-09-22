import subprocess
import time

LOG_FILE = "auth_log.txt"

print("=== AUTOMATED FIREWALL ENFORCEMENT ENGINE ENGAGED ===")
print(" [ MONITORING ] Watching log streams for active brute-force vectors...\n")

# 1. Read our active local threat logs
with open(LOG_FILE, "r") as file:
    log_lines = file.readlines()
    
for line in log_lines:
    # 2. Isolate high-velocity malicious login attempts
    if "STATUS:FAILED" in line:
        parts = line.split(" - ")
        ip_address = parts[1].replace("IP:", "").strip()
        
        rule_name = f"Banned_Hacker_{ip_address}"  # Clean name without embedded single quotes
        print(f"[ THREAT DETECTED ] Malicious activity tracked from: {ip_address}")
        
        # CHECK: Does this rule already exist?
        check_command = ["netsh", "advfirewall", "firewall", "show", "rule", f"name={rule_name}"]
        result = subprocess.run(check_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if result.returncode == 0:
            print(f"[ SKIPPED ] {ip_address} is already blocked. Moving on...\n")
            continue
            
        # 3. Deploy the rule if it doesn't exist
        print(f"[ ACTION ] Deploying rule to drop all incoming packets from {ip_address}...")
        
        firewall_command = [
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name={rule_name}",
            "dir=in",
            "action=block",
            f"remoteip={ip_address}"
        ]
        
        subprocess.run(firewall_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[ SUCCESS ] Firewall rule locked! {ip_address} is permanently banned.\n")
        time.sleep(1)
