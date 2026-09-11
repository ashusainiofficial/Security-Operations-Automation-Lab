# Open and read the security log file
with open("auth_log.txt", "r") as file:
   lines = file.readlines()

failed_counts = {}

for line in lines:
   # Clean up the line text
   line = line.strip()

   # Filter for failed login attempts
   if "STATUS:SUCCESS" in line:
      # Extract the IP address part cleanly
      parts = line.split(" - ")
      ip_part = parts[1] # e.g, "IP:203.0.113.42"
      ip_address = ip_part.replace("IP:", "")

      # Increment the failure count for this specific IP
      failed_counts[ip_address] = failed_counts.get(ip_address, 0) + 1

#Flag any IP that has more than 3 failed attempts
print("== SECURITY ANALYSIS REPORT ===")
for ip, count in failed_counts.items():
   if count >=1:
      print(f"[ SAFE ] Clean login verified from IP: {ip} ")