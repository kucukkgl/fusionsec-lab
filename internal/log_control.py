# internal/log_control.py

from flask import request, jsonify
import logging


def register_log_routes(app):

    @app.get("/internal/log/level")
    def get_log_level():
        level = logging.getLogger().getEffectiveLevel()
        return jsonify({"level": logging.getLevelName(level)})

    @app.post("/internal/log/level")
    def set_log_level():
        level = request.args.get("level", "").upper()

        valid = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        if level not in valid:
            return jsonify({
                "error": "invalid level",
                "valid_levels": valid
            }), 400

        logging.getLogger().setLevel(level)

        return jsonify({
            "status": "ok",
            "new_level": level
        })

    @app.get("/internal/log/volcano")
    def log_volcano():
        """
        Generates a burst of logs at all levels.
        Perfect for teaching log noise, filtering, and detection engineering.
        """
        logger = logging.getLogger("volcano")

        logger.debug("Volcano DEBUG event")
        logger.info("Volcano INFO event")
        logger.warning("Volcano WARNING event")
        logger.error("Volcano ERROR event")
        logger.critical("Volcano CRITICAL event")

        return jsonify({"status": "volcano_triggered"})
