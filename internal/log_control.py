import logging
from flask import Blueprint, request

log_control_blueprint = Blueprint("log_control", __name__)

# ---------------------------------------------------------
# Map string levels to logging constants
# ---------------------------------------------------------
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

# ---------------------------------------------------------
# Endpoint: change global log level
# ---------------------------------------------------------
@log_control_blueprint.route("/set_level", methods=["GET"])
def set_level():
    level_name = request.args.get("level", "info").lower()

    if level_name not in LOG_LEVELS:
        logging.error(f"Invalid log level requested: {level_name}")
        return f"Invalid log level: {level_name}"

    new_level = LOG_LEVELS[level_name]
    logging.getLogger().setLevel(new_level)

    logging.info(f"Log level changed to: {level_name.upper()}")
    return f"Log level set to {level_name.upper()}"
