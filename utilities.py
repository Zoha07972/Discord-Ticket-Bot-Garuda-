# -----------------------------------------------------------------------------
# File Name   : utilities.py
# Description : Loads and validates environment-backed Discord channel and role configuration.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               
                                                                               

import logging

import os


logger = logging.getLogger(__name__)

def _id(name: str, default: str = "0") -> int:
    raw = os.getenv(name, default).strip()
    try:
        return int(raw or "0")
    except ValueError as exc:
        raise RuntimeError(f"{name} must be a Discord numeric ID, got {raw!r}") from exc


ALLOWED_CHANNEL_ID = _id("ALLOWED_CHANNEL_ID")
TICKET_MESSAGE_CHANNEL_ID = _id("TICKET_MESSAGE_CHANNEL_ID")
TICKET_LOG_CHANNEL_ID = _id("TICKET_LOG_CHANNEL_ID")
SUPPORT_ROLE_ID = _id("SUPPORT_ROLE_ID")
SALES_ROLE_ID = _id("SALES_ROLE_ID")
NETWORK_ROLE_ID = _id("NETWORK_ROLE_ID")
GARUDA_ROLE_ID = _id("GARUDA_ROLE_ID")
DATABASE_BACKUP_FOLDER = os.getenv("DATABASE_BACKUP_FOLDER", "./ticket_backups")
os.makedirs(DATABASE_BACKUP_FOLDER, exist_ok=True)


def validate_config() -> None:
    required = {
        "ALLOWED_CHANNEL_ID": ALLOWED_CHANNEL_ID,
        "TICKET_LOG_CHANNEL_ID": TICKET_LOG_CHANNEL_ID,
        "SUPPORT_ROLE_ID": SUPPORT_ROLE_ID,
        "SALES_ROLE_ID": SALES_ROLE_ID,
        "NETWORK_ROLE_ID": NETWORK_ROLE_ID,
        "GARUDA_ROLE_ID": GARUDA_ROLE_ID,
    }
    missing = [name for name, value in required.items() if value <= 0]
    if missing:
        raise RuntimeError("Configure these Discord IDs in .env before starting: " + ", ".join(missing))
