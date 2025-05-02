import json
import os

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print("[!] config.json not found. Please enter your Telegram API credentials.")
        api_id = int(input("Enter your API ID: "))
        api_hash = input("Enter your API Hash: ").strip()
        save_config(api_id, api_hash)
    else:
        with open(CONFIG_FILE, 'r') as file:
            try:
                config_data = json.load(file)
                print(f"[+] Loaded config: {config_data}")  # Debugging line
                api_id = config_data.get("api_id")
                api_hash = config_data.get("api_hash")
            except json.JSONDecodeError as e:
                print(f"[!] JSONDecodeError: {e}")
                return None, None  # In case the JSON is corrupted
    return api_id, api_hash
