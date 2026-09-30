# Wireshark Display Filter Cheat Sheet

This reference document outlines the primary display filters utilized by L1 SOC Analysts and Incident Responders to isolate traffic anomalies, investigate protocols, and detect active threats within network packet captures (PCAPs).

---

## 🌐 1. IP & Core Network Layer Filters
Use these to filter traffic by specific endpoints, subnets, or communication pathways.

- `ip.addr == 192.168.1.1` — Displays all packet streams involving this specific IP address as a source or destination.
- `ip.src == 10.0.0.5` — Filters for traffic originating exclusively from this source IP address.
- `ip.dst == 8.8.8.8` — Filters for traffic traveling exclusively to this destination IP address.
- `ip.addr == 192.168.1.0/24` — Monitors an entire network range or subnet block simultaneously.
- `not ip.addr == 192.168.1.5` — Hides a specific machine's safe background traffic to eliminate investigation noise.

---

## 🚪 2. Port & Transport Layer Filters
Use these to target targeted communications infrastructure and audit standard application doors.

- `tcp.port == 22` — Filters for SSH traffic (Remote server administration consoles).
- `tcp.port == 21` — Filters for FTP traffic (Plain-text file movements).
- `tcp.port == 23` — Filters for Telnet traffic (Insecure, unencrypted remote terminal control).
- `tcp.port == 3389` — Filters for RDP traffic (Remote Desktop Protocol connections).
- `udp.port == 53` — Filters for DNS traffic (Domain Name System infrastructure queries).
- `tcp.port == 80 || tcp.port == 443` — Displays standard web traffic (HTTP and HTTPS) concurrently.

---

## 🕵️‍♂️ 3. HTTP & Plain-Text Forensic Filters
Use these to identify unencrypted credential transmissions, data leakage, and web directory brute-forcing.

- `http.request.method == "POST"` — Isolates outbound web form submissions (such as login fields or file uploads).
- `http.request.method == "GET"` — Displays client requests for web pages, images, or remote assets.
- `http.request` — Views all outgoing HTTP requests while suppressing server responses.
- `http.response.code == 404` — Tracks "Page Not Found" server errors. Mass spikes indicate automated directory scanning.
- `http contains "password"` — Scans raw payload packets for literal string indicators like "password" or "username".

---

## 🛡️ 4. Advanced Threat & Protocol Filters
Use these to capture reconnaissance signatures, network routing manipulation, or system mapping attempts.

- `tcp.flags.syn == 1 and tcp.flags.ack == 0` — Identifies active TCP connection requests. Spikes indicate an active port scanning sweep.
- `dns.flags.response == 1` — Isolates return responses from upstream DNS servers.
- `icmp` — Filters for Ping requests, unreachable nodes, and structural network telemetry.
- `arp` — Monitors Address Resolution Protocol broadcasts to detect internal local spoofing attacks.

---

## 🔀 5. Logical Combination Operators
Combine parameters to isolate multi-variable security incidents:

- `and` / `&&` — Both conditions must be met:
  `ip.src == 192.168.1.50 && tcp.port == 22`
- `or` / `||` — Either condition can be met:
  `udp.port == 53 || icmp`
- `not` / `!` — Excludes a condition:
  `tcp.port == 80 and not ip.addr == 192.168.1.1`

---

## 💡 The Golden Rule of Forensic Analysis
Once a suspicious protocol packet line is flagged in your interface view:
1. **Right-click** the target line.
2. Navigate to **Follow**.
3. Select **TCP Stream**.
This stitches the fragmented packet frames into a human-readable text dashboard, exposing plain-text credential leaks or malicious commands.

