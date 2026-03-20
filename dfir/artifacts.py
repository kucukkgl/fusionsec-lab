from flask import jsonify, request
import os
import datetime

ARTIFACT_DIR = "dfir_artifacts"

def register_dfir_routes(app):

    @app.get("/dfir/user_action")
    def dfir_user_action():
        action = request.args.get("action", "unknown")
        timestamp = datetime.datetime.now().isoformat()

        os.makedirs(ARTIFACT_DIR, exist_ok=True)
        filename = os.path.join(ARTIFACT_DIR, f"{timestamp}.txt")

        with open(filename, "w") as f:
            f.write(f"User action: {action}\nTimestamp: {timestamp}\n")

        return jsonify({"status": "ok", "action": action})
