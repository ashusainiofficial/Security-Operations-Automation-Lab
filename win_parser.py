#Open and read the raw windows Security event log
with open("win_log.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    
print ("===WINDOWS LOGON AUDIT REPROT ===")
failed_count = 0
success_count = 0

for line in lines:
    # Winoes event log fields are seprated by tab characters(\t)
    columns = line.strip().split("\t")
    
    # Ensure the line has enough columns to avoid errors
    if len(columns) > 3:
        event_id = columns[3].strip() # The Event ID column
        
        # Event 4625 = Failed Logon Attempt
        if event_id == "4625":
            failed_count += 1
            print(f"[FAILED LOGON] Event detected at: {columns[1]}")
            
        # Event 4624 = Successful Logon Attempt
        elif event_id == "4624":
            success_count += 1
             
print("\n=== SYSTEM OVERVIEW ===")
print(f"Total Successful Logins: {success_count}")
print(f"Total Failed Logins: {failed_count}")

if failed_count > 5:
    print("[ ALERT ] High volume of failed logons! Check for active brute-force threat.")
elif failed_count > 0:
    print("[ LOW WARNING] Minor login failure detected. Normal user typo.")