# 📑 Standard Operating Procedure (SOP): Brute-Force Triage & Remediation
**Document ID:** SOC-SOP-2026-004  
**Classification:** Internal Corporate Security Document  
**Target Threat Profiles:** High-Velocity Authentication Anomalies & Scheduled Botnet Vectors

---

## 🛑 Phase 1: Identification & Query Optimization
When automated alerts signal suspicious authentication failures, the responding L1/L2 SOC Analyst must execute a targeted database triage sweep immediately.

1. **Restrict the Index Scope:** Avoid expensive `index=*` queries to protect server memory limits. Isolate the target infrastructure bucket cleanly:
   `index=linux_secure sourcetype=secure-2 "Failed password"`
2. **Execute Velocity Assessment:** Run the baseline aggregation matrix to calculate attack counts:
   `| stats count as total_attempts by src_ip | sort - total_attempts`
3. **Analyze Time Trends:** Bucket the authentication metrics chronologically to confirm if the attack is human-driven or script-automated:
   `| timechart span=1h count by username useother=f limit=5`

*If the timeline displays tight chronological alignment (e.g., massive velocity spikes peaking at the exact same hour across multiple days), immediately classify the incident as an **Automated Cron-Job / Botnet Infiltration Attempt**.*

---

## 🔍 Phase 2: Containment & Application-Layer Filtering
Once the malicious source IP addresses are isolated, containment must be deployed immediately to safeguard core network endpoints.

1. **Extract Hidden Variables:** If source IPs are trapped inside unstructured text fields, deploy regular expression digital scalpels to format the dataset:
   `| rex "from (?<attacker_ip>\d+\.\d+\.\d+\.\d+)"`
2. **Deploy Application-Layer Protection:** Fire the automated firewall engine script (`auto_blocker.py`) to read incoming logs and dynamically construct blocking chains:
   `netsh advfirewall firewall add rule name="Banned_Hacker_[IP]" dir=in action=block remoteip=[IP]`
3. **Implement Deduplication Filters:** Ensure the tracking loops leverage an in-memory set object to block identical threat vector entries at the script layer, avoiding firewall table resource exhaustion.

---

## 🔒 Phase 3: Root-Cause Infrastructure Hardening
Dropping the attacker's IP at the perimeter is temporary. The analyst must actively modify the target server properties to eliminate the underlying vulnerability completely.

1. **Access Master Configuration Controls:** Access the endpoint terminal architecture directly:
   `sudo nano /etc/ssh/sshd_config`
2. **Disable Administrative Access Vectors:** Locate `PermitRootLogin` and toggle the parameter to `no` to strip away default profile exposure targets.
3. **Mandate Cryptographic Key Handshakes:** Locate `PasswordAuthentication` and toggle the parameter to `no`. This mandates multi-bit cryptographic key validation files (.pem/.pub), rendering automated text dictionary scripts completely obsolete.
