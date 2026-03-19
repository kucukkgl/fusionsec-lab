import argparse
from flask import Flask

from pentest.sqli import sqli_blueprint
from pentest.session_hijack import session_blueprint

from dfir.artifacts import dfir_blueprint

from internal.fim import fim_blueprint
from internal.log_control import log_blueprint

from logging_config import setup_logging



def create_app():
    app = Flask(__name__)

    app.register_blueprint(sqli_blueprint, url_prefix="/pentest/sqli")
    app.register_blueprint(session_blueprint, url_prefix="/pentest/session")

    app.register_blueprint(dfir_blueprint, url_prefix="/dfir")

    app.register_blueprint(fim_blueprint, url_prefix="/internal/fim")
    app.register_blueprint(log_blueprint, url_prefix="/internal/log")

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

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind the server to"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to run the server on"
    )

    return parser.parse_args()

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    setup_logging()          # initialize logging first
    args = get_arguments()
    app = create_app()
    app.run(host=args.host, port=args.port)
