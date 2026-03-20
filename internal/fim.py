import os
import datetime
from flask import jsonify, request

BASE_DIR = "fim"

def ensure_dirs():
    os.makedirs(f"{BASE_DIR}/created", exist_ok=True)
    os.makedirs(f"{BASE_DIR}/modified", exist_ok=True)
    os.makedirs(f"{BASE_DIR}/deleted", exist_ok=True)
    os.makedirs(f"{BASE_DIR}/uploaded", exist_ok=True)
    os.makedirs(f"{BASE_DIR}/beacon", exist_ok=True)

def write_event(folder, filename):
    ensure_dirs()
    timestamp = datetime.datetime.now().isoformat()
    path = f"{BASE_DIR}/{folder}/{timestamp}_{filename}"
    with open(path, "w") as f:
        f.write(f"Event: {folder}\nFilename: {filename}\nTimestamp: {timestamp}\n")
    return path

def register_fim_routes(app):

    @app.get("/internal/fim/create")
    def fim_create():
        filename = request.args.get("filename", "unknown.txt")
        write_event("created", filename)
        return jsonify({"status": "created", "filename": filename})

    @app.get("/internal/fim/modify")
    def fim_modify():
        filename = request.args.get("filename", "unknown.txt")
        write_event("modified", filename)
        return jsonify({"status": "modified", "filename": filename})

    @app.get("/internal/fim/delete")
    def fim_delete():
        filename = request.args.get("filename", "unknown.txt")
        write_event("deleted", filename)
        return jsonify({"status": "deleted", "filename": filename})

    @app.get("/internal/fim/upload")
    def fim_upload():
        filename = request.args.get("filename", "unknown.txt")
        write_event("uploaded", filename)
        return jsonify({"status": "uploaded", "filename": filename})

    @app.get("/internal/fim/beacon")
    def fim_beacon():
        write_event("beacon", "heartbeat")
        return jsonify({"status": "beacon"})
