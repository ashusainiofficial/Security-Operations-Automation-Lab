# Project Name: Enterprise SIEM Threat Hunting Lab (Splunk Cloud)
**Author:** ronaldo.paccione  
**Target Focus:** SIEM Ingestion, Advanced SPL Queries, Incident Triage, and Forensic Field Extraction  
**Framework Alignment:** MITRE ATT&CK Matrix (Discovery T1033 / PowerShell Execution T1059.001)

---

## 📋 Executive Incident Summary
During an architecture review of a simulated enterprise network domain (`PASCALPIG`), a high-priority alert threshold was breached triggering an investigation into the master system logs. An unindexed data pool containing **7,718 complex structural system logs** was parsed using customized parsing configurations within an active **Splunk Cloud instance**. 

Through iterative search filtering and raw string identification patterns, a malicious deployment pipeline was isolated. The attacker successfully ran initial endpoint reconnaissance scripts (`HOSTNAME.EXE`, `whoami.exe`) and bypassed local safety boundaries by forcing automated PowerShell cryptographic network overrides (`Tls12`).

---

## 🔬 Practical Lab Architecture & Data Flow
1. **Log Data Collection Engine:** System Monitor (Sysmon) operational text array capturing endpoint process creation events.
2. **SIEM Analytics Infrastructure:** Active Splunk Cloud instance running custom ingestion mapping rules.
3. **Primary Data Repository:** `index=main` 
4. **Custom Schema Driver:** `sourcetype=sysmon` (Configured manually via raw XML auto-text parser logic).

---

## 🛠️ Step-by-Step Execution & Advanced SPL Code

### 1. The Initial XML Structural Fix
Because raw endpoint data is structured natively inside dense, unparsed XML text arrays containing structural element markers like `<EventID>1</EventID>`, traditional field filtering initially generated clean null responses. To bypass this database constraint, an explicit wildcard text-search filter was deployed to hunt the exact process creation footprint:

```text
index=main sourcetype=sysmon "<EventID>1</EventID>"
```

### 2. Forensic Regex Field Extraction (`rex`)
To turn messy, unstructured text string layers into a highly polished, scannable corporate evidence spreadsheet, an advanced regular expression processing pipe (`| rex`) was formulated. This logic dynamically targets the text strings sitting between the `CommandLine'>` properties and the terminal `<` tag boundaries, isolating the clean executed scripts into a dedicated runtime array named `CMD`:

```text
index=main sourcetype=sysmon "<EventID>1</EventID>" 
| rex field=_raw "CommandLine'>(?<CMD>[^<]+)" 
| table _time, host, CMD
```

---

## 🕵️‍♂️ Unmasked Attacker Actions & Evidence Profiling

The regular expression pipeline successfully extracted the exact forensic proofs of the attacker's timeline behavior:

### Evidence Item A: Host Reconnaissance
* **Extracted Script:** `C:\Windows\system32\HOSTNAME.EXE`
* **Analyst Evaluation:** The adversary queried the local machine name immediately upon entry. This aligns with **MITRE ATT&CK T1033 (System Owner/User Discovery)**. The hacker used this to map target assets and confirm if they landed on high-value corporate servers or standard nodes.

### Evidence Item B: Privilege Level Discovery
* **Extracted Script:** `"C:\Windows\system32\whoami.exe"`
* **Analyst Evaluation:** The adversary evaluated active terminal privilege boundaries. Identifying whether the compromised context was a restricted user account or an administrative role allows the attacker to decide if a follow-up Privilege Escalation attack vector is required.

### Evidence Item C: The Encrypted Network Connection String (Smoking Gun)
* **Extracted Script:** `"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" & {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12`
* **Analyst Evaluation:** This represents the definitive **MITRE ATT&CK T1059.001 (PowerShell Execution)** breach footprint. The attacker explicitly initiated a system override to mandate `Tls12` encryption protocols across the session pipeline. This guarantees their outbound callback scripts can talk safely to external malicious Command-and-Control (C2) servers without failing due to outdated legacy corporate security handshakes.

---

## 📊 Operational Threat Hunting Dashboard Assembly
To guarantee these complex forensic indicators are never lost in basic terminal run histories, the final stage of the lab sequence focused on assembling an enterprise-grade **Incident Threat Hunting Dashboard** using **Splunk Classic Dashboard** frames.

* **Widget Layout:** Suspicious PowerShell Monitoring Grid
* **Panel Configuration:** Custom-extracted text rows mapped neatly to an interactive **Statistics Table** displaying a live, chronological stream of active system command overrides for security remediation teams.

## 🖼️ Verified Lab Deployment View
![Incident Monitoring Dashboard](assets/dashboard.png)

![Incident Monitoring Dashboard](assets/dashbord1.png)

![Incident Monitoring Dashboard](assets/dashbord2.png)


### 📊 3. Enterprise Splunk Cloud Threat Hunting & Behavioral Analytics Engine
- **Data Ingestion Scale:** Ingested and indexed **117,729 real-world production events** from the official Splunk Boss of the SOC (BOTS) database cluster, mapping multi-server log structures (`www1`, `www3`, `mailsv`, `vendor_sales`).
- **Advanced SIEM Search Queries Engineered:**
  - *Web Server Directory Reconnaissance Scan:*
    `index=* sourcetype=access_combined_wcookie status=404 | top uri`
  - *Brute-Force Account Target Triage via Custom Regex:*
    `index=* sourcetype=secure-2 "Failed password" | rex "Failed password for\s+(invalid user\s+)?(?<username>\S+)" | top username`
  - *Attacker Infrastructure Source Tracking via Custom Regex:*
    `index=* sourcetype=secure-2 "Failed password" | rex "from (?<attacker_ip>\d+\.\d+\.\d+\.\d+)" | top attacker_ip`
  - *Chronological Threat Velocity & Trend Analysis:*
    `index=* sourcetype=secure-2 "Failed password" | rex "Failed password for\s+(invalid user\s+)?(?<username>\S+)" | timechart span=1h count by username useother=f limit=5`
- **Automated Threat Intelligence Discovery:** Leveraged `timechart` analytics to isolate a massive, synchronized authentication anomaly. The engine proved that brute-force attempts targeting the **`root`** account were not manual human interactions, but rather an **automated, script-driven botnet (Cron-job)** executing exactly at **10:00 PM daily** with a velocity spike exceeding 200 events per hour.
- **Visual Intelligence Output:** Compiled a centralized **SOC Threat Operations Center Dashboard** hosting three interconnected behavioral panels translating 33,253 raw attack sequences into visual metrics tracking targeted users, malicious source IPs, and hourly trend velocities.

![SOC Threat Operations Center Dashboard](assets/splunk_dashboard.png)
