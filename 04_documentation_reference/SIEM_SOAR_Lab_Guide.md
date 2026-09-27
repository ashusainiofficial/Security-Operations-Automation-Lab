# 📑 Production Blueprints: Distributed Endpoint SIEM/SOAR Engineering Lab

## 🗺️ Architectural Topology
```
[ Windows 11 Laptop ] 
       │
       ├──► (Local Event Logging Engine) ──► Event ID 4625 (Security Log)
       │
       ├──► (Splunk Universal Forwarder) ──► TLS Port 9997 ──► [ Splunk Cloud SIEM ] (Sandbox/Read-Only)
       │
       └──► (Custom Python Alert Agent) ──► HTTPS Port 443 ──► [ Shuffle SOAR Cloud Canvas ] (Status: 200 OK)
```

---

## 🛠️ Phase 1: Ingestion Target Preparation (Shuffle SOAR Workspace)
Before routing endpoint telemetry, a target landing zone must be constructed within the automation layer.

1. Navigate to `https://shuffler.io` and create a free tier workspace account.
2. From the left-hand navigation sidebar, click on the **Workflows** module icon.
3. Click the orange `+ New Workflow` button in the upper right quadrant.
4. Set workspace metadata parameters:
   * **Name:** `Live_Windows_Threat_Response`
   * **Description:** `Automated ingestion and enrichment of endpoint brute force alerts.`
5. Click **Create from scratch** on the subsequent pop-up prompt to instantiate a blank orchestration canvas.
6. Expand the **Triggers** drawer panel on the left sidebar framework.
7. Click and drag the **Webhook** module element onto the blank grid infrastructure.
8. Click directly on the newly dropped **Webhook block** to initialize its properties panel on the right flank.
9. Locate the **Webhook URL** field string (e.g., `https://shuffler.io/api/v1/hooks/webhook_xxxxxxxxxx`) and click the orange **Copy** button. Keep this workspace tab open.
10. Highlight the default orange template app block titled `"Change Me"` on the canvas, press `Delete` on your keyboard, and click the orange **Save** button at the base toolbar to lock in a clean workspace layout.

---

## 📥 Phase 2: SIEM Agent Integration & Administrative Password Override
This phase converts your local computer asset into a managed endpoint tracking node, routing encrypted streams to the cloud indexer.

### Step 1: Secure Cloud Credential Acquisition
1. Authenticate into your web-based **Splunk Cloud Platform** web console dashboard.
2. Access the navigation framework pane and select **Apps** ➡️ **Universal Forwarder**.
3. Execute the action link for **Download Universal Forwarder Credentials**.
4. A cryptographically signed configuration package container file labeled **`splunkclouduf.spl`** will download. Save this directory package exclusively to your laptop's localized `Downloads` or drive root path (e.g., `D:\splunkclouduf.spl`). *Do not extract or modify this file container.*

### Step 2: Agent Installation
1. Obtain the **Splunk Universal Forwarder (Windows 64-bit MSI)** installation bin package from the official Splunk distribution portal.
2. Initialize the `.msi` binary execution wrapper.
3. Agree to the formal licensing frameworks.
4. When prompted to generate local administrator console credentials for the local engine daemon, choose an administrative user string (e.g., `admin`). *If the installer auto-generates a randomized masked string, proceed through the setup wizard to complete installation.*
5. In the log subscription menu checklist pane, mark the radial options for **Application**, **Security**, and **System** logs. Finish the install wrapper steps.

### Step 3: Hard Overriding Locked / Lost Agent Credentials
If a randomized administrative access password string was populated by the initial installation wizard, the Command Line Interface (CLI) configuration toolset will throw local authentication verification failures. Bypassing this requires an internal system configuration file reset:

1. Click the Windows Start key, type `cmd`, right-click **Command Prompt**, and select **Run as administrator**.
2. Terminate the active local log forwarding daemon by executing:
   ```cmd
   net stop SplunkForwarder
   ```
3. Purge the operational encrypted security credential database file containing the randomized keys by executing:
   ```cmd
   del "C:\Program Files\SplunkUniversalForwarder\etc\passwd"
   ```
4. Inject a clean user seed file directive into the system path to specify your own manual authentication parameters:
   ```cmd
   notepad "C:\Program Files\SplunkUniversalForwarder\etc\system\local\user-seed.conf"
   ```
5. Notepad will prompt to instantiate a new document structure. Click **Yes** and paste the exact configuration stanzas:
   ```ini
   [user_info]
   USERNAME = admin
   PASSWORD = YourCustomSecurePassword123!
   ```
6. Write changes to the block using `Ctrl + S` and close Notepad.
7. Re-initialize the localized infrastructure monitoring engine:
   ```cmd
   net start SplunkForwarder
   ```
   *Upon service initialization, the engine natively parses the plain-text `user-seed.conf` profile rules, updates the cryptographic `passwd` database with the custom hash credentials, and safely deletes the cleartext file automatically for security.*

### Step 4: Cryptographic Cloud Handshake Execution
With the password override functional, hand over the cloud security application package keys to the local system forwarder toolset:

1. In the administrative terminal window, shift your current processing directory to the core forwarder execution path:
   ```cmd
   cd "C:\Program Files\SplunkUniversalForwarder\bin"
   ```
2. Feed your previously downloaded cloud credentials bundle to the application management system (modify the target path link to point to where your specific `.spl` package resides):
   ```cmd
   splunk.exe install app "D:\splunkclouduf.spl"
   ```
3. The prompt interface will prompt for access credentials. Use the manually forced profile data:
   * **Splunk username:** `admin`
   * **Password:** `YourCustomSecurePassword123!`
4. Upon receiving the success confirmation output (`App '...' installed`), restart the application service layer:
   ```cmd
   splunk.exe restart
   ```

---

## ⚙️ Phase 3: Telemetry Stream Management (`inputs.conf`)
Bypassing graphical installer options via administrative resets strips default channel settings. The forwarder must be explicitly instructed on which local Event Viewer channels to read.

1. Launch a new elevated terminal window or maintain your existing administrative Command Prompt workspace.
2. Create or override the system log input instructions by running:
   ```cmd
   notepad "C:\Program Files\SplunkUniversalForwarder\etc\system\local\inputs.conf"
   ```
3. Erase all text errors inside and overwrite with this exact enterprise-grade log parsing manifest:
   ```ini
   [default]
   host = MyPersonalLaptop

   [WinEventLog://Security]
   disabled = 0
   index = main
   start_from = oldest
   current_only = 0

   [WinEventLog://System]
   disabled = 0
   index = main
   start_from = oldest
   current_only = 0

   [WinEventLog://Application]
   disabled = 0
   index = main
   start_from = oldest
   current_only = 0
   ```
4. Save file adjustments and close the window framework.
5. Command the local daemon to process the modified log streaming layout policies instantly:
   ```cmd
   "C:\Program Files\SplunkUniversalForwarder\bin\splunk.exe" restart
   ```

---

## 🔍 Phase 4: SIEM Ingestion Verification Metrics
Confirm that your local workstation telemetry is successfully clearing local perimeter controls and parsing into the remote SIEM indices.

1. Navigate back to the web browser interface pane for your **Splunk Cloud console**.
2. Open the **Search & Reporting** workspace core application view.
3. In the text processing search bar execution frame, enter the wide search index query:
   ```splunk
   index=main
   ```
4. Shift the active processing time boundary picker dropdown from *Last 24 Hours* to **Last 15 minutes** or **Preset ➡️ Last 60 minutes**.
5. Execute the search action. Validate that events populated exhibit a row metrics tally count greater than `0` and verify the `host` key maps cleanly to `MyPersonalLaptop`.

---

## 🌐 Phase 5: Troubleshooting Cloud Sandbox Network Boundaries
With data streams populating the SIEM, we attempted to configure a real-time automated webhook correlation alert pointing from Splunk Cloud to Shuffle SOAR. 

### 🛑 Infrastructure Roadblock Discovered
1. **The Architecture Issue:** While Splunk Cloud successfully compiled and indexed threat match counts (e.g., *7 results scanned from 98 events*), the outbound network packets never reached the Shuffle SOAR servers.
2. **Root Cause Analysis:** Splunk Cloud Free Trials drop outbound webhook payloads by default to mitigate threat manipulation or malicious relay misuses. Access keys to modify the **Server Settings ➡️ Webhook Allow List** dashboard are systematically hidden or omitted from standard public trial sandboxes.

### 🛠️ Strategic Remediation: Engineering a Local Broker Agent Proxy
To bypass this multi-cloud network barrier, you engineered a custom telemetry broker agent script using **Python**. This agent functions as a proxy threat reporter, packaging your structural intrusion variables and delivering them directly across port 443 into the active SOAR engine canvas.

1. Right-click on your Windows laptop **Desktop**, select **New ➡️ Text Document**, and change the complete extension naming profile structure to **`soar_alert_agent.py`** (ensure it does not end in `.txt`).
2. Open the script wrapper container in Notepad, copy and paste this exact production payload module framework, and **replace the web address variable** with your exact Shuffle Webhook URL:
   ```python
   import json
   import requests

   # Paste your unique Shuffle Webhook URL between the quotes below
   SHUFFLE_WEBHOOK_URL = "https://shuffler.io/api/v1/hooks/webhook_YOUR_ACTUAL_URL_HERE"

   alert_data = {
       "message": "Failed Windows login detected",
       "event": 4625,
       "user": "HackerAttackerAccount"
   }

   try:
       response = requests.post(SHUFFLE_WEBHOOK_URL, json=alert_data, headers={"Content-Type": "application/json"})
       print(f"Status Code: {response.status_code}")
       print("Response text:", response.text)
   except Exception as e:
       print(f"Delivery failed: {e}")
   ```
3. Save file modifications (`Ctrl + S`) and close out the terminal.

---

## 💥 Phase 6: Operationalizing the Live Attack Simulation Loop

### Step 1: Active Ingestion Verification
1. Access your **Shuffle SOAR Canvas** web interface tab.
2. Look at the base command control toolbar workspace pane. Find the orange **Start/Play** toggle icon to activate the webhook interface daemon listener.
3. Click the orange **Save** icon layout to commit changes.
4. Click on the **Running Person** icon block right next to it to display the execution history pane stream.

### Step 2: Live Intruder Threat Footprint Generation
1. Launch your administrative Windows **Command Prompt** framework.
2. Force the generation of authentic local cryptographic intrusion audit logs (**Event Code 4625 - Failed Authentication**) by executing this command exactly three times:
   ```cmd
   runas /user:HackerAttackerAccount cmd
   ```
3. When requested for an administrative verification string key, type any random collection of letters and hit **Enter**. The security core engine will immediately write a critical logon failure metric into the local Windows Security event viewer pool.

### Step 3: Launching the Telemetry Alert Broker Agent
1. In your command line interface terminal workspace window, adjust your terminal directory context directly to your Desktop path space:
   ```cmd
   cd %USERPROFILE%\Desktop
   ```
2. Execute the python automated alert agent application script tool to bridge the data across the open internet:
   ```cmd
   python soar_alert_agent.py
   ```
3. **Validate terminal output response values:** The application window output will return an explicit connection code payload confirmation:
   ```cmd
   Status Code: 200
   Response text: {"success": true, "execution_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}
   ```

### Step 4: Capturing the Live Execution metrics within the SOAR Interface
1. Return instantly to your open **Shuffle SOAR canvas window tab**.
2. Inspect the **Running Person history tracking logs list panel**.
3. A distinct row displaying a **green successful completion tag** matching your exact execution ID token string will render.
4. Click on the green event entry row line. Review the internal parsed metrics array window pane to verify your laptop's custom telemetry components populate live variables inside the active workspace container:
   ```json
   {
     "message": "Failed Windows login detected",
     "event": 4625,
     "user": "HackerAttackerAccount"
   }
   ```