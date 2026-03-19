from flask import Blueprint, jsonify, request
import os
import datetime

dfir_blueprint = Blueprint("dfir", __name__)

ARTIFACT_DIR = "dfir_artifacts"

@dfir_blueprint.route("/dfir/user_action")
def user_action():
    action = request.args.get("action", "unknown")
    timestamp = datetime.datetime.now().isoformat()

    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    filename = os.path.join(ARTIFACT_DIR, f"{timestamp}.txt")
    with open(filename, "w") as f:
        f.write(f"User action: {action}\nTimestamp: {timestamp}\n")

    return jsonify({"status": "ok", "action": action})
