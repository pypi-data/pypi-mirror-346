import subprocess
import sys
import platform

def install_amazon_q():
    system_platform = platform.system()

    if system_platform == "Darwin":  # macOS
        try:
            # Check if Amazon Q is already installed
            result = subprocess.run(["q", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Amazon Q is already installed.")
            else:
                print("❌ Amazon Q is not installed. Installing via Homebrew...")
                subprocess.check_call(["brew", "install", "amazon-q"])
                print("✅ Amazon Q installed successfully.")
        except FileNotFoundError:
            # If `q` command is not found, install using Homebrew
            print("❌ Amazon Q is not installed. Installing via Homebrew...")
            subprocess.check_call(["brew", "install", "amazon-q"])
            print("✅ Amazon Q installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing Amazon Q: {e}")
            sys.exit(1)

    elif system_platform == "Windows":  # Windows
        print("❌ Amazon Q is not supported directly on Windows via pip.")
        print("Please download and install Amazon Q from the official site:")
        print("🔗 https://aws.amazon.com/q/")
        print("Follow the instructions on the website to download and install Amazon Q.")
        sys.exit(1)

    else:  # Linux or other OSes
        print("❌ Unsupported OS detected. Amazon Q installation only supported on macOS.")
        sys.exit(1)
