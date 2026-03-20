import argparse
from flask import Flask, render_template

from pentest.sqli import register_sqli_routes
from pentest.session_hijack import register_session_routes
from internal.fim import register_fim_routes
from internal.log_control import register_log_routes
from dfir.artifacts import register_dfir_routes

from logging_config import setup_logging


def create_app():
    app = Flask(__name__)

    # Register all modules (no blueprints)
    register_sqli_routes(app)
    register_session_routes(app)
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
    app.run(host=args.host, port=args.port)
