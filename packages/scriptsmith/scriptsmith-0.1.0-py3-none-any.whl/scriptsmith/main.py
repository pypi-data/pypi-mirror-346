import os
import pdb
import sys
import json
import subprocess
import click
from supabase import create_client
from dotenv import load_dotenv
from scriptsmith.setup import setup_scriptsmith, get_supabase_client,load_config
import shlex
import threading
import time

# Load environment variables from .env file
load_dotenv()

def show_spinner(message="Running..."):
    spinner = "|/-\\"
    idx = 0
    while not stop_spinner.is_set():
        print(f"\r{message} {spinner[idx % len(spinner)]}", end="", flush=True)
        idx += 1
        time.sleep(0.1)
    print("\r", end="")  # Clean up line when done

stop_spinner = threading.Event()
spinner_thread = threading.Thread(target=show_spinner)

# Supabase client initialization
# SUPABASE_URL = os.environ.get("SUPABASE_URL")
# SUPABASE_KEY = os.environ.get("SUPABASE_KEY")



# If no credentials are found, exit
# if not SUPABASE_URL or not SUPABASE_KEY:
#     print("Error: SUPABASE_URL and SUPABASE_KEY must be set in a .env file.")
#     sys.exit(1)

# # Create the Supabase client using the credentials from .env
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@click.group()
def cli():
    """ScriptSmith CLI main entry point."""
    pass


@cli.command()
def setup():
    """
    Run the interactive setup for ScriptSmith.
    """
    setup_scriptsmith()


@cli.command()
@click.argument("description")
@click.option("--schedule", default=None, help="Cron schedule (e.g. \"0 0 * * *\"). Stored for future reference.")
def create_task(description, schedule):
    """
    Create a new task with a natural language description (prompt). Optionally include a cron schedule.
    """
    task = {
        "description": description,
        "schedule": schedule or ""
    }
    supabase = get_supabase_client()
    try:
        response = supabase.table("tasks").insert(task).execute()

        # import pdb; pdb.set_trace()
    except Exception as e:
        print(f"Error during task creation: {e}")
        sys.exit(1)

    # Check for error in response
    if response is None:
        print(f"Error during task creation: {response.data}")
        sys.exit(1)

    # If successful, print the task ID
    print(f"Task created successfully with ID {response}.")

@cli.command()
def list_tasks():
    """
    List all tasks from the Supabase table.
    """
    supabase = get_supabase_client()
    try:
        response = supabase.table("tasks").select("id, description, schedule").execute()
    except Exception as e:
        print(f"Error retrieving tasks: {e}")
        sys.exit(1)

    if response != 200:
        print(f"Error retrieving tasks: {response.data}")
        sys.exit(1)

    tasks = response.data
    if not tasks:
        print("No tasks found.")
        return

    print("Tasks:")
    for task in tasks:
        task_id = task.get("id")
        description = task.get("description")
        schedule = task.get("schedule") or "None"
        print(f"- ID: {task_id} | Description: {description} | Schedule: {schedule}")


@cli.command()
@click.argument("task_id", type=int)
def run_task(task_id):
    """
    Run a task by ID: send its description as a prompt to the Amazon Q CLI and capture the generated script.
    """
    supabase = get_supabase_client()

    try:
        task_resp = supabase.table("tasks").select("*").filter("id", "eq", task_id).execute()
    except Exception as e:
        print(f"Error fetching task: {e}")
        sys.exit(1)

    task_data = task_resp.data
    if not task_data:
        print(f"Task ID {task_id} not found.")
        return

    task = task_data[0]
    prompt = task.get("description")

    if not prompt:
        print("Task has no description/prompt.")
        return
    print(f"Running task {task_id} with prompt: {prompt}")
    # Start the spinner
    stop_spinner = threading.Event()

    def show_spinner(message="Running..."):
        spinner = "|/-\\"
        idx = 0
        while not stop_spinner.is_set():
            print(f"\r{message} {spinner[idx % len(spinner)]}", end="", flush=True)
            idx += 1
            time.sleep(0.1)
        print("\r", end="")  # Clean up the line when done

    spinner_thread = threading.Thread(target=show_spinner)
    spinner_thread.start()

    try:
        # Run the Amazon Q command
        command = f"q chat --trust-all-tools --no-interactive -- {shlex.quote(prompt)}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    finally:
        # Stop the spinner
        stop_spinner.set()
        spinner_thread.join()


    # try:
    # # Load configuration to get the Builder ID
    #     config = load_config()
    #     builder_id = config.get("AMAZON_Q_BUILDER_ID")

    #     if not builder_id:
    #         print("❌ Builder ID not found in configuration. Run 'scriptsmith setup' to initialize.")
    #         sys.exit(1)

    #     # Run the Amazon Q command with the Builder ID
    #     command = f"q chat --trust-all-tools --no-interactive --builder-id {shlex.quote(builder_id)} -- {shlex.quote(prompt)}"
    #     result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # finally:
    #     # Stop the spinner
    #     stop_spinner.set()
    #     spinner_thread.join()

    # Process the result
    if result.returncode != 0:
        print(f"❌ Amazon Q CLI error:\n{result.stderr}")
        log_entry = {
            "task_id": task_id,
            "script": f"ERROR: {result.stderr}"
        }
    else:
        script_output = result.stdout.strip()
        print("✅ Generated script:")
        print(script_output)
        log_entry = {
            "task_id": task_id,
            "script": script_output
        }

    # Store the result in logs
    try:
        log_resp = supabase.table("logs").insert(log_entry).execute()
        print(f"📝 Script and log saved for task {task_id}.")
    except Exception as e:
        print(f"⚠️ Failed to save log: {e}")

if __name__ == "__main__":
    cli()