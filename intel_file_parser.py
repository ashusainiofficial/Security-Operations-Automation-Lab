# 1. Read the external threat database file
with open ("blacklist.txt", "r") as file:
    # Read all lines and strip out white space/newlines using a list comprehension
    threat_feed = [line.strip() for line in file.readlines()]

# 2. Set an incoming IP to test
incoming_ip = "185.220.101.5"

print("=== LIVE FILE THREAT AUDIT ===")

if incoming_ip in threat_feed:
    print(f"[ ALERT ] Critical match! {incoming_ip} is a known malicious source.")
else:
    print(f"[ SAFE ] {incoming_ip} cleared.")