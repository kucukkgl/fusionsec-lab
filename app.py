import argparse
from flask import Flask, render_template, request, g
import threading
import logging
import secrets
import time
from datetime import datetime, timezone


from pentest.sqli import register_sqli_routes
from pentest.session_hijack import register_session_routes
from pentest.login import home_page_login
from internal.fim import register_fim_routes
from internal.log_control import register_log_routes
from dfir.artifacts import register_dfir_routes
from host_manager.c2_connector import pingit
from host_manager.c2_connector import daily_message_thread

from logging_config import setup_logging


def create_app():
    app = Flask(__name__)

    @app.before_request
    def log_request():
        g.cid = secrets.token_hex(6)
        g.request_start = time.perf_counter()

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        username = "-"
        if request.method == "POST":
            username = request.form.get("username", "-")

        logging.info(
            f'event=request_received '
            f'timestamp={timestamp} '
            f'cid={g.cid} '
            f'ip={request.remote_addr} '
            f'method={request.method} '
            f'uri={request.path} '
            f'qs="{request.query_string.decode()}" '
            f'ua="{request.user_agent.string}" '
            f'referer="{request.referrer or ""}" '
            f'user="{username}" '
            f'body=""'
        )
    @app.after_request
    def log_response(response):
        latency_ms = int(
            (time.perf_counter() - g.request_start) * 1000
        )

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        response_size = response.calculate_content_length()
        if response_size is None:
            response_size = 0

        logging.info(
            f'event=response_sent '
            f'timestamp={timestamp} '
            f'cid={g.cid} '
            f'ip={request.remote_addr} '
            f'status="{response.status}" '
            f'latency_ms={latency_ms} '
            f'response_size={response_size}'
        )

        return response
    # Register all modules (no blueprints)
    register_sqli_routes(app)
    register_session_routes(app)
    home_page_login(app)
    register_fim_routes(app)
    register_log_routes(app)
    register_dfir_routes(app)

    # Homepage
    @app.route("/")
    def index():
        return render_template("index.html")

    # Health endpoints
    @app.route("/health")
    def health():
        return "OK"

    @app.route("/status")
    def status():
        return "running"

    @app.route("/version")
    def version():
        return "1.0"

    return app


def get_arguments():
    parser = argparse.ArgumentParser(description="FusionSec Lab Server")

    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)

    return parser.parse_args()


if __name__ == "__main__":
    setup_logging()
    args = get_arguments()
    app = create_app()
    threading.Thread(target=pingit, daemon=True).start()
    threading.Thread(target=daily_message_thread, daemon=True).start()

    app.run(host=args.host, port=args.port)

