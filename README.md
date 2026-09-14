# Security Operations & Threat Intelligence Lab

This repository contains custom Python automation tools engineered to ingest system logs, parse complex text strings, and correlate them against open-source intelligence feeds.

## Projects Included

### 1. Windows Endpoint Auditor (win_parser.py)
- **Purpose:** Automatically scans raw system metrics exported from the Windows Event Viewer.
- **Key Feature:** Implements a two-tier automated threat alert engine to catch failed logon attempts and reduce alert fatigue.

### 2. Live Dynamic SIEM Engine (live_siem.py)
- **Purpose:** Connects to the internet via HTTP streams to download live threat databases.
- **Key Feature:** Uses header spoofing to ingest active hacker IP addresses from TweetFeed Live safely.

## How to Run the Tools

To execute the live SIEM engine on your local machine, open your terminal and run:
```bash
python live_siem.py
```
