import logging
from logging.handlers import RotatingFileHandler
import os
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_record)

def setup_logging():
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    plain_log_path = "logs/app.log"
    json_log_path = "logs/app_log.json"

    # Rotating file handler for Plain Logs (20 KB for fast rotation in labs)
    plain_log_file_handler = RotatingFileHandler(
        plain_log_path,
        maxBytes=20000,
        backupCount=5
    )
    plain_log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    plain_log_file_handler.setFormatter(plain_log_formatter)

    # JSON Logs (20 KB for fast rotation in labs)
    json_log_file_handler = RotatingFileHandler (
        json_log_path,
        maxBytes=20000,
        backupCount=5
    )
    json_log_formatter = JsonFormatter()
    json_log_file_handler.setFormatter(json_log_formatter)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(plain_log_file_handler)
    logger.addHandler(json_log_file_handler)

    # Console output for real-time feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(plain_log_formatter)
    logger.addHandler(console_handler)

    logging.info("FusionSec Lab logging initialized")
