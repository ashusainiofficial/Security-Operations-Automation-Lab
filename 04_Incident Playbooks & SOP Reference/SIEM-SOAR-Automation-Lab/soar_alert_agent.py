import time
import re
import urllib.parse
import json
import requests
import subprocess
import sys
from flask import Flask, request
import logging
import threading  # <-- Add this!

# 1. Your Shuffle Webhook_1 URL (For sending alerts)
SHUFFLE_WEBHOOK_URL = "https://shuffler.io/api/v1/hooks/webhook_a10e269c-ecc3-4f6b-bf1c-85d8eb0ec86f"

app = Flask(__name__)

# Suppress standard web server logs to keep terminal clean
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def fire_alert(target_ip="176.113.115.105"):
    print(f"\n📡 Attempting to fire alert telemetry to Shuffle for {target_ip}...")
    alert_data = {
        "message": "Failed Windows login detected",
        "event": 4625,
        "user": "HackerAttackerAccount",
        "source_ip": target_ip
    }
    
    try:
        response = requests.post(SHUFFLE_WEBHOOK_URL, json=alert_data, headers={"Content-Type": "application/json"})
        print(f"📡 [INGEST] Telemetry packet delivered to SOAR. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ [ERROR] Ingest delivery failed: {e}")

def execute_containment_block(target_ip):
    print(f"🚨 [MITIGATION] CONTAINMENT INSTRUCTION EXECUTING: Blocking malicious IP {target_ip}...")
    
    # Bulletproof PowerShell check: Assign rule to variable, check if it equals $null
    powershell_cmd = (
        f'$rule = Get-NetFirewallRule -DisplayName "SOAR_Automated_Block_{target_ip}" -ErrorAction SilentlyContinue; '
        f'if ($null -eq $rule) {{ '
        f'New-NetFirewallRule -DisplayName "SOAR_Automated_Block_{target_ip}" -Direction Inbound -Action Block -RemoteAddress {target_ip} | Out-Null; '
        f'Write-Host "CREATED" '
        f'}} else {{ Write-Host "EXISTS" }}'
    )
    
    try:
        # We drop check=True so Python doesn't crash if PowerShell throws a soft warning
        result = subprocess.run(["powershell", "-Command", powershell_cmd], capture_output=True, text=True)
        
        # Explicitly verify PowerShell's exact output string
        if "EXISTS" in result.stdout:
            print(f"🛡️ [SKIPPED] Firewall rule for {target_ip} already exists. No duplicate created.")
        elif "CREATED" in result.stdout:
            print(f"🔒 [SUCCESS] Windows Advanced Firewall updated. Remote Address {target_ip} is now permanently blocked!")
        else:
             print(f"⚠️ [WARNING] Unexpected PowerShell behavior. Output: {result.stdout.strip()} | Error: {result.stderr.strip()}")
             
    except Exception as e:
        print(f"❌ [ERROR] Firewall rule injection failed: {e}")

def monitor_security_logs():
    print("👁 [TELEMETRY] Live Windows Event Viewer monitoring started. Hunting for Event 4625...")
    
    # Baseline setup: Query the current newest event ID so old events are ignored
    init_cmd = "powershell -Command \"Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 1 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty RecordId\""
    init_res = subprocess.run(init_cmd, capture_output=True, text=True, shell=True)
    
    try:
        last_record_id = int(init_res.stdout.strip())
        print(f"📌 [BASELINE] Monitoring established. Ignoring events prior to Record ID: {last_record_id}")
    except (ValueError, TypeError):
        last_record_id = None
        print("📌 [BASELINE] No prior Event 4625 records detected. Listening for incoming events...")

    while True:
        try:
            cmd = "powershell -Command \"Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 1 -ErrorAction SilentlyContinue | Select-Object -Property RecordId, Message | ConvertTo-Json\""
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            if result.stdout.strip():
                import json
                event = json.loads(result.stdout)
                current_record_id = event.get("RecordId")
                
                if current_record_id and (last_record_id is None or current_record_id > last_record_id):
                    # Immediately update tracking pointer to prevent duplicate processing loops
                    last_record_id = current_record_id
                    
                    message = event.get("Message", "")
                    ip_match = re.search(r"Source Network Address:\s*([^\r\n]+)", message)
                    
                    attacker_ip = "176.113.115.105" # Default test IP
                    if ip_match:
                        raw_ip = ip_match.group(1).strip()
                        if raw_ip not in ["-", "127.0.0.1", "::1"]:
                            attacker_ip = raw_ip
                        else:
                            print(f"\n⚠️ [TEST MODE] Local logon detected. Remapping '{raw_ip}' to simulated attacker: {attacker_ip}")
                    
                    print(f"🚨 [DETECTION] New Event 4625 (Record {current_record_id})! Triggering pipeline...")
                    fire_alert(attacker_ip)
                    
        except Exception as e:
            print(f"⚠️ [MONITOR ERROR] Telemetry parsing failure: {e}")
            
        time.sleep(5)
        
# This is the permanent endpoint that Shuffle will push data directly to!
@app.route('/mitigate', methods=['POST'])
def mitigate_threat():
    data = request.json
    if data and "target_ip" in data:
        raw_target = data["target_ip"]
        response_url = None  # Initialize the URL variable
        
        # --- DEFENSIVE EXTRACTION ---
        if "%7B" in raw_target or "block_actions" in raw_target:
            try:
                decoded_text = urllib.parse.unquote(raw_target)
                import json
                slack_json = json.loads(decoded_text)
                malicious_ip = slack_json["actions"][0]["value"]
                
                # 🎯 GRAB THE SECRET SLACK URL
                response_url = slack_json.get("response_url") 
                
            except Exception as e:
                print(f"❌ [ERROR] Could not parse Slack payload: {e}")
                return {"status": "failed", "error": "Parse error"}, 400
        else:
            malicious_ip = raw_target
        # -----------------------------
            
        print(f"\n📥 [DIRECT INGEST] Command received from Slack to block: {malicious_ip}")
        
        # 1. Run the slow PowerShell command in the background
        threading.Thread(target=execute_containment_block, args=(malicious_ip,)).start()
        
        # 2. OVERWRITE THE SLACK UI (The State Lock)
        if response_url:
            print("🔄 Updating Slack UI to prevent duplicate clicks...")
            slack_update = {
                "replace_original": "true",
                "text": f"🚨 *SOC ALERT RESOLVED*\n• *Target:* MyPersonalLaptop\n• *Attacker IP:* {malicious_ip}\n• *Status:* 🔒 CONTAINED (Firewall Block Active)"
            }
            try:
                requests.post(response_url, json=slack_update)
            except Exception as e:
                print(f"⚠️ [WARNING] Could not update Slack UI: {e}")
        
        print("⚡ Acknowledging Slack instantly to prevent timeout...")
        return {"status": "success"}, 200
        
    return {"status": "failed", "error": "No IP provided"}, 400

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--listen":
        print("🤖 [AGENT] SOAR Active Containment Push Receiver is running on Port 5000...")
        
        # Start the Event Viewer monitor in the background!
        threading.Thread(target=monitor_security_logs, daemon=True).start()
        
        print("⏳ Waiting for direct analyst authorization from Slack...")
        app.run(port=5000)
    else:
        # Keep this for manual testing if you ever need it
        fire_alert("9.9.9.9")