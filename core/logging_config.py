# -----------------------------------------------------------------------------
# File Name   : logging_config.py
# Description : Configures shared console and rotating-file logging for the bot.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               

                                                                               

import logging
import os
from logging.handlers import RotatingFileHandler


logger = logging.getLogger(__name__)

def configure_logging() -> None:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    os.makedirs(os.getenv("LOG_DIR", "logs"), exist_ok=True)
    log_file = os.path.join(os.getenv("LOG_DIR", "logs"), "ticket-bot.log")

    root = logging.getLogger()
    root.setLevel(level)
    if root.handlers:
        return

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root.addHandler(console)
    root.addHandler(file_handler)
