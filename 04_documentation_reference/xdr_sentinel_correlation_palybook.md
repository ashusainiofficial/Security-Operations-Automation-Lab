# 📡 Microsoft Sentinel Cross-Domain XDR Correlation Playbook
**Document ID:** SOC-XDR-2026-009  
**Target Focus:** Cross-Domain Analytics, KQL Pipeline Optimization, and Lateral Threat Tracking  
**Framework Alignment:** MITRE ATT&CK Matrix (Phishing T1566 / PowerShell T1059.001 / Exfiltration T1567)

---

## 📋 Architectural Design Overview
Traditional monitoring structures fail when tracking sophisticated adversaries who pivot laterally across isolated infrastructure silos. This playbook engineers a cross-domain correlation model within **Microsoft Sentinel** utilizing **Kusto Query Language (KQL)** to automatically stitch identity anomalies, local endpoint process creations, and cloud storage manipulations into a single consolidated incident timeline.

---

## 🛠️ Production KQL Correlation Rule Code
```kusto
let InboundPhishing = SigninLogs | where ResultType == 0 | where LocationDetails.countryOrRegion != "IN" | project TimeGenerated, UserPrincipalName, AttackerIP = IPAddress;
let EndpointMalware = DeviceProcessEvents | where ProcessCommandLine contains "powershell.exe" and ProcessCommandLine contains "Tls12" | project ProcessTime = TimeGenerated, AccountName, DeviceName, ProcessCommandLine;
let CloudExfiltration = AzureActivity | where OperationNameValue == "Microsoft.Storage/storageAccounts/blobServices/containers/write" | project StorageTime = TimeGenerated, CallerEmail = Caller, StorageAccount = Resource;
InboundPhishing
| join kind=inner EndpointMalware on left.UserPrincipalName == right.AccountName
| join kind=inner CloudExfiltration on left.UserPrincipalName == right.CallerEmail
| where ProcessTime between (TimeGenerated .. datetime_add('minute', 30, TimeGenerated))
| project TimeGenerated, UserPrincipalName, AttackerIP, DeviceName, ProcessCommandLine, StorageAccount
```

---

## 🎙️ Natural-Language Interview Cheat Codes
When an interviewer queries your understanding of advanced cross-domain correlation or Sentinel engineering, land these punchy keyword anchors:
- **"Infrastructure Silos"** — The separate identity, endpoint, and cloud environments that attackers exploit.
- **"Cross-Domain KQL Joins"** — Utilizing Kusto Query Language mapping properties to link data points over a shared user variable.
- **"Microsecond Lateral Visibility"** — Automatically compressing multi-stage attacks into a single incident to slash investigation intervals.
