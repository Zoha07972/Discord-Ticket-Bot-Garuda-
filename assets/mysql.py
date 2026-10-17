# -----------------------------------------------------------------------------
# File Name   : mysql.py
# Description : Provides async MySQL connections and initializes the ticket schema.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               


import logging
import os
import re
from pathlib import Path

import aiomysql

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = PROJECT_ROOT / "schema.sql"


async def get_database_connection():
    """Return a database connection, or None when connection setup fails."""
    required = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        logger.error("Database configuration is missing: %s", ", ".join(missing))
        return None

    try:
        return await aiomysql.connect(
            host=os.environ["DB_HOST"],
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            db=os.environ["DB_NAME"],
            autocommit=False,
            connect_timeout=int(os.getenv("DB_CONNECT_TIMEOUT", "10")),
            charset="utf8mb4",
        )
    except Exception:
        logger.exception("Failed to connect to the ticket database")
        return None


async def initialize_database() -> None:
    if not SCHEMA_PATH.is_file():
        raise FileNotFoundError(f"Database schema file was not found: {SCHEMA_PATH}")

    connection = await get_database_connection()
    if connection is None:
        raise RuntimeError("Could not connect to the ticket database; startup aborted.")

    try:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        statements = [statement.strip() for statement in schema.split(";") if statement.strip()]
        async with connection.cursor() as cursor:
            for statement in statements:
                match = re.match(
                    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?([A-Za-z0-9_]+)`?",
                    statement,
                    flags=re.IGNORECASE,
                )
                if match:
                    table_name = match.group(1)
                    await cursor.execute(
                        "SELECT 1 FROM information_schema.tables "
                        "WHERE table_schema = DATABASE() AND table_name = %s LIMIT 1",
                        (table_name,),
                    )
                    if await cursor.fetchone():
                        logger.debug("Database table '%s' already exists; skipping creation", table_name)
                        continue
                await cursor.execute(statement)
        await connection.commit()
        logger.info("Database schema verified; missing ticket tables were created if necessary")
    except Exception:
        await connection.rollback()
        logger.exception("Failed to initialize ticket database schema")
        raise
    finally:
        connection.close()
