import os
import sys
import json
from supabase import create_client
import subprocess
from .utils import install_amazon_q

CONFIG_FILE = os.path.expanduser("~/.scriptsmith_config.json")
_supabase_client = None  # Singleton instance


def save_config(url, key):
    try:
        config = {
            "SUPABASE_URL": url,
            "SUPABASE_KEY": key,
            # "AMAZON_Q_BUILDER_ID": builder_id
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

    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        sys.exit(1)


def get_supabase_client():
    """
    Returns a configured Supabase client.
    This function will cache the client instance for future use.
    """
    global _supabase_client

    if _supabase_client is not None:
        return _supabase_client

    config = load_config()
    if not config:
        print("❌ No configuration found. Run 'scriptsmith setup' to initialize.")
        sys.exit(1)

    url = config.get("SUPABASE_URL")
    key = config.get("SUPABASE_KEY")

    try:
        _supabase_client = create_client(url, key)
        return _supabase_client
    except Exception as e:
        print(f"❌ Failed to create Supabase client: {e}")
        sys.exit(1)


def setup_scriptsmith():
    """
    Interactive setup for configuring ScriptSmith.
    """
    print("\n🔧 ScriptSmith Setup\n")
    url = input("Enter your Supabase URL: ").strip()
    key = input("Enter your Supabase Key: ").strip()
    # builder_id = input("Enter your Amazon Q Builder ID: ").strip()

    # Save the configuration
    save_config(url, key)
    install_amazon_q()

    # Initialize Supabase client to verify connection
    supabase = get_supabase_client()
    if not supabase:
        print("❌ Failed to connect to Supabase. Check your URL and Key.")
        sys.exit(1)

    # Check if user is logged in to Amazon Q
    try:
        result = subprocess.run(["q", "whoami"], capture_output=True, text=True)
        if result.returncode != 0:
            print("🔑 Logging into Amazon Q...")
            subprocess.run(["q", "login"], input="Use for Free with Builder ID\n", text=True)
            print("✅ Amazon Q login complete.")
        else:
            print("✅ You are already logged in to Amazon Q.")
    except Exception as e:
        print(f"❌ Error during Amazon Q login: {e}")
        sys.exit(1)

    print("\n🎉 Setup complete. You are ready to use ScriptSmith!")

