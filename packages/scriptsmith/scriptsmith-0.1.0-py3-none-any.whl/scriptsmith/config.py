import os
import json
import sys

CONFIG_FILE = os.path.expanduser("~/.scriptsmith_config.json")

def save_config(url, key, builder_id):
    try:
        config = {
            "SUPABASE_URL": url,
            "SUPABASE_KEY": key,
            "AMAZON_Q_BUILDER_ID": builder_id
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        print("✅ Configuration saved successfully.")
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")
        sys.exit(1)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print("⚠️ No configuration found. Run 'scriptsmith setup' to initialize.")
        return None

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def get_supabase_client():
    config = load_config()
    if not config:
        print("⚠️ Supabase credentials not found. Run 'scriptsmith setup' first.")
        return None

    from supabase import create_client
    return create_client(config["SUPABASE_URL"], config["SUPABASE_KEY"])