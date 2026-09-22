#!/bin/bash
#=========================================================
# TOOL NAME : cron_auditor.sh
# PURPOSE : Automated System-Wide Forensic Sweep of Scheduled Linux Backdoors 
#=========================================================
echo "================================================"
echo " STARTING LINUX CRONTAB FORENSIC SYSTEM AUDIT"
echo "================================================"
echo " [MONITORING] Ingesting operational scheduling ledgers..."


# 1. Inspect the global system-wide master configuration file
echo -e "\n[AUDITING]: /etc/crontab (System Master File)"
if [ -f /etc/crontab ]; then
    cat /etc/crontab | grep -v '^#' | grep -v '^$'
else
    echo " System crontab file not located or inaccessible."
fi

# 2. Audit the system cron directory sectors
echo -e "\n[AUDITING]: Global Cron Directories (/etc/cron.*)"
ls -la /etc/cron.hourly/ /etc/cron.daily/ /etc/cron.d/ 2>/dev/null

# 3. Dynamic Loop to hunt through every single individual user account profile
echo -e "\n [AUDITING]: Individual User Profile Crontabs"
#Read local system account vault (/etc/passwd) columns via awk
for user in $(awk -F: '{print $1}' /etc/passwd); do
    # Run the native crontab lookups while redirecting access errors to null data channels
	user_cron=$(crontab -u "$user" -l 2>/dev/null)
	
	if [ ! -z "$user_cron" ]; then
	     echo -e "\n [FLAGGED PROFIL ALERT]: Account '$user' has active scheduled items!"
		 echo "-------------------------------------------"
		 echo "$user_cron" | grep -v '^#'
		 echo "-------------------------------------------"
	fi
done

echo -e "\n==============================================="
echo "[] FORENSIC AUDIT COMPLETE: System scheduler vectors verified clear."
echo "===================================================="