# -----------------------------------------------------------------------------
# File Name   : main.py
# Description : Application entry point for the Garuda Cloud Discord ticket bot.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               

                                                                               

import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

from core.logging_config import configure_logging              

configure_logging()
logger = logging.getLogger(os.getenv("LOGGER_NAME", "garudacloud.ticketbot").strip() or "garudacloud.ticketbot")

TOKEN = os.getenv("DISCORD_BOT_TOKEN", "").strip()
if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is missing. Set it in your environment or .env file.")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class TicketBot(commands.Bot):
    async def setup_hook(self) -> None:
                                                                                  
        from utilities import validate_config
        validate_config()
        from assets.mysql import initialize_database
        await initialize_database()
        from ticket_system.ticket_system import setup as setup_ticket_system
        await setup_ticket_system(self)
        try:
            synced = await self.tree.sync()
            logger.info("Synced %s application command(s).", len(synced))
        except discord.DiscordException:
            logger.exception("Failed to sync application commands")
            raise

    async def on_ready(self) -> None:
        logger.info("Ticket bot connected as %s (ID: %s).", self.user, self.user.id if self.user else "unknown")


bot = TicketBot(command_prefix="!", intents=intents)


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: Exception) -> None:
    logger.error("Application command failed", exc_info=(type(error), error, error.__traceback__))
    message = "Something went wrong while running that command. Please try again or contact staff."
    try:
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)
    except discord.NotFound:
        logger.warning("Could not respond to an expired interaction.")
    except discord.HTTPException:
        logger.exception("Could not deliver application-command error response")


if __name__ == "__main__":
    logger.info("Starting Garuda Cloud Ticket Bot")
    bot.run(TOKEN, log_handler=None)
