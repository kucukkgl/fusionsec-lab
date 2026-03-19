import logging
from flask import Blueprint, request
import os
import datetime

fim_blueprint = Blueprint("fim", __name__)

# ---------------------------------------------------------
# Directory structure for FIM artifacts
# ---------------------------------------------------------
FIM_DIR = "fim"
SUBDIRS = ["created", "modified", "deleted", "uploaded", "beacon"]

# Ensure directories exist (cross‑platform)
os.makedirs(FIM_DIR, exist_ok=True)
for sub in SUBDIRS:
    os.makedirs(os.path.join(FIM_DIR, sub), exist_ok=True)


# ---------------------------------------------------------
# Helper: write a FIM artifact file
# ---------------------------------------------------------
def write_fim_event(event_type, filename, details):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    # Cross‑platform path construction
    path = os.path.join(FIM_DIR, event_type, f"{timestamp}_{filename}.txt")

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"timestamp={timestamp}\n")
        f.write(f"event_type={event_type}\n")
        f.write(f"filename={filename}\n")
        f.write(f"details={details}\n")

    logging.info(f"FIM event created: {path}")
    return path


# ---------------------------------------------------------
# Instructor-only FIM inject endpoint
# ---------------------------------------------------------
@fim_blueprint.route("/inject", methods=["GET"])
def inject_event():
    event_type = request.args.get("type", "created")
    filename = request.args.get("file", "note.txt")
    details = request.args.get("details", "no details provided")

    if event_type not in SUBDIRS:
        logging.error(f"Invalid FIM event type: {event_type}")
        return "Invalid event type"

    path = write_fim_event(event_type, filename, details)
    return f"FIM event created: {path}"
