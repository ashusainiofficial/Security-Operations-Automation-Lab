#!/bin/bash
#=========================================================
# TOOL NAME : cron_auditor.sh
# PURPOSE : Automated System-Wide Forensic Sweep of Scheduled Linux Backdoors
#=========================================================

echo "=============================================="
echo " STARTING LINUX CRONTAB FORENSIC SYSTEM AUDIT"
echo "=============================================="
echo "[ MONITORING ] Ingesting operational scheduling ledgers..."

# Clear the terminal and announce the audit sweep
print("=== NATIVE LINUX AUTOMATION AUDIT ENGAGED ===")

# 1. Inspect the global system-wide crontab file for unauthorized tasks
cat /etc/crontab

# 2. List every hidden execution script inside the daily/hourly system folders

ls -la /etc/cron.daily
ls -la /etc/cron.hourly

# 3. For loop to dynamically audit every single individual user account profile file
for user in $(awk -F: '{print $1} /etc/passwd); do
    print "[ AUDITING USER]: $user"
	crontab -u $user -l 2>/dev/null
done

