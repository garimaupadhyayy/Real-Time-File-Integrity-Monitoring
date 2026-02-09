import os
import hashlib
import json
import time
import logging
import smtplib
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


logging.basicConfig(
    filename="alerts.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s")

def send_email_alert(subject, body):
    try:  
        msg = EmailMessage()

        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        print("Email alert sent successfully!")

    except Exception as e:
        print("Failed to send email:", e)

def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print("Hash error:", e)
    return None
def scan_directory(directory):
    file_hashes = {}

    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            file_hash = calculate_hash(path)
            if file_hash:
                file_hashes[path] = file_hash

    return file_hashes

def save_baseline(hashes, baseline_file):
    with open(baseline_file, "w") as f:
        json.dump(hashes, f, indent=4)


def load_baseline(baseline_file):
    if not os.path.exists(baseline_file):
        return None
    with open(baseline_file, "r") as f:
        return json.load(f)

def compare_hashes(old_hashes, new_hashes):
    modified = 0
    deleted = 0
    added = 0

    
    for file_path, old_hash in old_hashes.items():
        if file_path not in new_hashes:
            alert = f"[ALERT] File deleted: {file_path}"
            print(alert)
            logging.info(alert)
            send_email_alert("File Deleted Alert", alert)
            deleted += 1

        elif file_path in new_hashes and new_hashes[file_path] != old_hash:
            alert = f"[ALERT] File modified: {file_path}"
            print(alert)
            logging.info(alert)
            send_email_alert("File Modified Alert", alert)
            modified += 1

   
    for file_path in new_hashes:
        if file_path not in old_hashes:
            alert = f"[ALERT] New file added: {file_path}"
            print(alert)
            logging.info(alert)
            send_email_alert("New File Added Alert", alert)
            added += 1

    if modified or deleted or added:
        print("\n===== Scan Summary =====")
        print(f"Modified files: {modified}")
        print(f"Deleted files: {deleted}")
        print(f"New files added: {added}\n")

def main():
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = input("Enter directory path to monitor: ")

    safe_dir_name = os.path.basename(os.path.normpath(directory))
    baseline_file = f"baseline_{safe_dir_name}.json"

    if not os.path.exists(directory):
        print("Invalid directory path.")
        return

    baseline = load_baseline(baseline_file)

    if baseline is None:
        print("Creating baseline...")
        baseline = scan_directory(directory)
        save_baseline(baseline, baseline_file)
        print("Baseline created successfully!")

    print("Real-time monitoring started (Checking every 10 seconds)...")
    print("Press Ctrl+C to stop.\n")

    while True:
        new_hashes = scan_directory(directory)
        compare_hashes(baseline, new_hashes)
        time.sleep(10)


if __name__ == "__main__":
    main()


