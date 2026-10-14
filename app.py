import argparse
import importlib
import os
from pathlib import Path
from flask import Flask, app, render_template, request, g
from flask.sessions import SecureCookieSessionInterface
import threading
import logging
import secrets
import time
from datetime import datetime, timezone

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = importlib.import_module("tomli")


from pentest.sqli import register_sqli_routes
from pentest.session_hijack import register_session_routes
from pentest.login import home_page_login
from pentest.signup import register_signup_routes
from pentest.admin import register_admin_routes
from internal.fim import register_fim_routes
from internal.log_control import register_log_routes
from dfir.artifacts import register_dfir_routes
from host_manager.c2_connector import pingit
from host_manager.c2_connector import daily_message_thread

from pentest.init_db import init_db
from logging_config import setup_logging


class LoggingSessionInterface(SecureCookieSessionInterface):
    def save_session(self, app, session, response):
        super().save_session(app, session, response)

        cookie_name = app.config["SESSION_COOKIE_NAME"]
        cookie_prefix = f"{cookie_name}="
        for header in response.headers.getlist("Set-Cookie"):
            if not header.startswith(cookie_prefix):
                continue

            cookie_value = header.partition(";")[0][len(cookie_prefix):]
            attributes = [part.strip() for part in header.split(";")[1:]]
            attributes_lower = [part.lower() for part in attributes]
            same_site = next(
                (
                    part.partition("=")[2]
                    for part in attributes
                    if part.lower().startswith("samesite=")
                ),
                "unset",
            )
            lifetime = (
                "cleared"
                if not cookie_value
                else (
                    "persistent"
                    if any(
                        part.startswith(("expires=", "max-age="))
                        for part in attributes_lower
                    )
                    else "browser-session"
                )
            )
            log_fields = (
                "event=session_cookie action=%s name=%s lifetime=%s "
                "httponly=%s secure=%s samesite=%s"
            )
            log_values = (
                "cleared" if not cookie_value else "issued",
                cookie_name,
                lifetime,
                "httponly" in attributes_lower,
                "secure" in attributes_lower,
                same_site,
            )
            if app.config["LOG_SESSION_COOKIE_VALUE"]:
                logging.warning(
                    f"{log_fields} value=%s",
                    *log_values,
                    cookie_value,
                )
            else:
                logging.info(
                    f"{log_fields} value_logged=false",
                    *log_values,
                )


def create_app():
    app = Flask(__name__)
    app.session_interface = LoggingSessionInterface()
    # Flask signs session cookies with SECRET_KEY; no custom cookie signer is needed.
    app.config["SECRET_KEY"] = (
        os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)
    )
    if not os.environ.get("FLASK_SECRET_KEY"):
        logging.warning(
            "FLASK_SECRET_KEY is unset; sessions will be invalidated on restart"
        )
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get(
            "SESSION_COOKIE_SECURE", "0"
        ).lower() in {"1", "true", "yes"},
    )

    app.config["TEMPLATES_AUTO_RELOAD"] = True
    with Path(__file__).with_name("pyproject.toml").open("rb") as project_file:
        project_config = tomllib.load(project_file)
    app.config["VERSION"] = project_config["project"]["version"]
    with Path(__file__).with_name("config.toml").open("rb") as config_file:
        runtime_config = tomllib.load(config_file)
    log_cookie_value = runtime_config.get("log_session_cookie_value", False)
    if not isinstance(log_cookie_value, bool):
        raise ValueError("log_session_cookie_value must be a TOML boolean")
    app.config["LOG_SESSION_COOKIE_VALUE"] = log_cookie_value
    if log_cookie_value:
        logging.warning(
            "Raw session-cookie logging is enabled; logs contain replayable credentials"
        )
    logging.info("Starting FusionSec Lab version=%s", app.config["VERSION"])

    init_db()

    # Default global state
    app.config["SQLI_LAB_MODE"] = "unsafe"

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
    register_admin_routes(app)
    home_page_login(app)
    register_signup_routes(app)
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
        return app.config["VERSION"]

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
