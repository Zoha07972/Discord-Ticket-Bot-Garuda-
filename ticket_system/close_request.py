# -----------------------------------------------------------------------------
# File Name   : close_request.py
# Description : Handles staff or customer requests to close a ticket with a reason.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               

                                                                               

import logging

import discord
from discord.ext import commands
from discord import app_commands
from assets.mysql import get_database_connection
from ticket_system.ticket_logging import log_ticket_close                    
from ticket_system.ticket_transcript import generate_transcript                       
from ticket_system.ticket_confirmation import CloseConfirmationView                                

logger = logging.getLogger(__name__)

class CloseRequest(commands.Cog):
   

    def __init__(self, bot: commands.Bot):
        self.bot = bot                               

    @app_commands.command(
        name="closerequest",
        description="Request to close the current ticket thread with a reason."
    )
    @app_commands.describe(reason="Specify a reason for closing the ticket.")
    @app_commands.checks.has_permissions(administrator=True)                                   
    async def close_request(self, interaction: discord.Interaction, reason: str = "No reason provided"):
        

                                                           
        await interaction.response.defer(ephemeral=False)

        thread = interaction.channel
        if not isinstance(thread, discord.Thread):
            await interaction.followup.send(
                "This command can only be used in ticket threads.",
                ephemeral=True
            )
            return

                                                   
        db_connection = await get_database_connection()
        opened_by = None

        if db_connection:
            try:
                async with db_connection.cursor() as cursor:
                    await cursor.execute(
                        "SELECT user_id FROM tickets WHERE channel_id = %s",
                        (thread.id,)
                    )
                    ticket_data = await cursor.fetchone()

                    if ticket_data:
                        opened_by = f"<@{ticket_data[0]}>"                            

            except Exception as e:
                logger.exception("Database error while looking up ticket owner")
            finally:
                db_connection.close()

                                    
        embed = discord.Embed(
            title="Close Request Initiated",
            color=discord.Color.orange(),
            description=(
                f"**Requested by:** {interaction.user.mention}\n"
                f"**Opened by:** {opened_by or 'Unknown'}\n"
                f"**Reason:** {reason}\n\n"
                "**Click 'Yes' to confirm ticket closure or 'No' to cancel.**"
            )
        )

                                                                          
        await interaction.followup.send(
            embed=embed,
            ephemeral=False,                                     
            view=CloseConfirmationView(reason=reason)
        )
