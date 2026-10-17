# -----------------------------------------------------------------------------
# File Name   : branding.py
# Description : Loads local Garuda Cloud branding assets for Discord embeds.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               


import logging
from pathlib import Path
from typing import Optional, Tuple

import discord

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = PROJECT_ROOT / "images"
LOGO_PATH = Path(__import__("os").getenv("LOGO_PATH", str(IMAGE_DIR / "garuda_logo.webp"))).expanduser()


def attach_logo(embed: discord.Embed) -> Tuple[discord.Embed, Optional[discord.File]]:
    if not LOGO_PATH.is_file():
        logger.debug("Local logo not found at %s; continuing without an embed image", LOGO_PATH)
        return embed, None

    embed.set_thumbnail(url="attachment://garuda_logo.webp")
    return embed, discord.File(LOGO_PATH, filename="garuda_logo.webp")
