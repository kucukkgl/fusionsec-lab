import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    log_path = "logs/app.log"

    # Rotating file handler (20 KB for fast rotation in labs)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=20000,
        backupCount=5
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # Console output for real-time feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logging.info("FusionSec Lab logging initialized")
