# 🪟 Windows PowerShell Event Log Forensics Cheat Sheet

This reference document catalogs essential native Windows PowerShell cmdlets and string-filtering pipelines used by L1/L2 Security Analysts to perform rapid endpoint triage, analyze authentication event IDs, and audit active network sockets.

---

## 🔑 Core Windows Security Event ID Reference
When auditing Windows Event Logs, look for these native numerical indicators:
- **Event ID 4624** — Successful Account Authentication (Safe User Activity).
- **Event ID 4625** — **Failed Account Authentication** (Footprint of a brute-force or credential-stuffing attack).
- **Event ID 4720** — A brand-new local user account was created (Potential adversary persistence mechanism).

---

## 📂 1. Low-Velocity File & String Triage
Use these short, easily memorized text filtering commands to scan raw export logs without administrative overhead.

- `Get-Content logfile.txt | Select-String 'EventID:4625'`
  - `Get-Content` — Streams a target text log file line by line.
  - `Select-String` — Extracts and displays lines matching the exact string argument (Failed Logins).

---

## 🛸 2. Advanced Native Event Log Extraction (Requires Admin Rights)
Use these high-speed XML-filtered pipelines when executing live forensic triage on an administrative terminal.

- `Get-WinEvent -LogName 'Security' -FilterXPath '*[System[(EventID=4625)]]' -MaxEvents 50`
  - `-LogName 'Security'` — Interfaces natively with the encrypted system security log architecture.
  - `-FilterXPath` — Employs direct database filtering query logic to bypass event indexing lag.
- `Get-WinEvent -LogName 'Security' -FilterXPath '*[System[(EventID=4720)]]'` — Automatically isolates all instances of local account creations to hunt for rogue backdoors.

---

## 🌐 3. Active Socket & Network Mapping
Trace local connections and mapping ports directly inside the PowerShell environment.

- `Get-NetTCPConnection -State Listen` — Displays all internal application ports actively waiting for incoming network connections.
- `Get-NetTCPConnection | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State` — Formats active socket configurations into a clean, human-readable operational table.
