# Security Operations & Threat Intelligence Lab

This repository contains custom security automation tools, enterprise data engineering frameworks, and threat hunting blueprints designed to ingest system logs, parse complex text strings, and correlate traffic metrics against live cyber threat vectors.

## Technical Projects Portfolio

### 1. Windows Endpoint Security Auditor (`win_parser.py`, `win_log.txt`)
- **Purpose:** Automatically scans and parses raw system metrics exported from the Windows Event Viewer.
- **Key Feature:** Implements a two-tier automated threat alert engine (`if/elif` conditional loops) to filter log data and reduce analyst alert fatigue by instantly distinguishing routine user typographical errors from high-velocity active brute-force threat vectors.

### 2. Live Dynamic Intelligence Ingestion Feed (`intel_parser.py`, `intel_file_parser.py`, `live_siem.py`)
- **Purpose:** Connects dynamically to open-source intelligence (OSINT) threat databases over the internet via encrypted HTTP streams.
- **Key Feature:** Progressed from basic local list membership lookups to an automated web-streaming engine utilizing custom header spoofing (User-Agent browser string replication) to safely download hundreds of active hacker IP indicators without triggering edge firewall drops.

### 3. Advanced Multi-Variable Incident Triage Application (`siem.py`, `advanced_siem.py`, `auth_log.txt`, `threat_report.csv`)
- **Purpose:** Processes complex security correlations by merging local system authentication logs with live web APIs and geographic directories.
- **Key Feature:** Integrates string stripping loops (`.strip()`) to eliminate log data whitespace formatting anomalies, executes live HTTP queries against the `ip-api.com` directory to extract geographic origin metrics, and automatically compiles structural spreadsheets (`threat_report.csv`) for incident response teams.

### 4. Enterprise Splunk Cloud Threat Hunting & Behavioral Analytics
- **Purpose:** Indexes large-scale corporate data environments (`tutorialdata.zip`) to track complex security anomalies and build visual operations rooms.
- **Key Feature:** Authored complex Search Processing Language (SPL) queries and Regular Expression (`rex`) digital extraction scalpels (`\S+`, `\d+`) to isolate variables out of raw text paragraphs. Successfully uncovered a high-velocity, automated cron-job botnet attack wave executing daily at 10:00 PM.

### 5. Live Local Network Packet Sniffer (`sniffer.py`)
- **Purpose:** Taps directly into the local physical network interface card to intercept traffic passing through the network adapter in real-time.
- **Key Feature:** Executes low-level socket interception using the Scapy library under Administrator privileges, filtering transport layer components dynamically to isolate unencrypted HTTP web portal interactions (Port 80).

### 6. Automated Firewall Enforcement Engine (`auto_blocker.py`)
- **Purpose:** Bridges log analysis with active infrastructure defense to neutralize attacks automatically in real-time.
- **Key Feature:** Scans incoming system authentication log streams, isolates malicious high-velocity brute-force IP addresses, and dynamically constructs and executes native Windows shell command sequences (`netsh advfirewall`) using Python's `os.system` hook to permanently drop all incoming attacker data packets.

### 7. Native Windows Event Log Forensic Tracker (`windows_powershell_cheatsheet.md`, `windows_simulated_log.txt`)
- **Purpose:** Leverages native Windows shell environments to parse structural authentication datasets and isolate system access failures.
- **Key Feature:** Formulates highly efficient, easily memorizable PowerShell pipelines using streaming utilities (`Get-Content`) and conditional text evaluation filters (`Select-String`) to isolate **Windows Event ID 4625 (Failed Authentication Footprints)**. This provides high-speed local endpoint triage capabilities without incurring the system resource overhead of a full graphical SIEM deployment.

---

## Operational Command Structure

To execute the data engines or the local packet sniffer within this sandbox laboratory toolkit, open your Git Bash terminal and run:

```bash
# To run the advanced threat triage application:
python advanced_siem.py

# To run the live packet sniffer (Requires Admin rights):
python sniffer.py
```
