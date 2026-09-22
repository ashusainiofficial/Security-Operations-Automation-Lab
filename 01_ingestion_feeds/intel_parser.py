# 1. Our Threat Intelligence Blocklist (Known Malicious Hackers_
blacklisted_ips = ["203.0.113.42", "198.51.100.15", "192.0.2.1"]

# 2. An incoming network IP caught attempting to connect to your software
incoming_ip = "192.168.1.1"

print("=== THREAT INTELLIGENCE AUDT ===")

if incoming_ip in blacklisted_ips:
    print(f"[ CRITICAL ALERT ] Connection blocked! IP {incoming_ip} matches global threat feed.")
else:
    print(f"[ CLEAN ] Traffic authorized. IP {incoming_ip} is not blacklisted.")