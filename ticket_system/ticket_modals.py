# -----------------------------------------------------------------------------
# File Name   : ticket_modals.py
# Description : Collects the ticket closure reason through a Discord modal.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               
                                                                               

import logging

import discord
from assets.mysql import get_database_connection
from ticket_system.ticket_confirmation import CloseConfirmationView

logger = logging.getLogger(__name__)

class CloseReasonModal(discord.ui.Modal, title="Close Ticket with Reason"):
    reason = discord.ui.TextInput(
        label="Reason", 
        style=discord.TextStyle.long, 
        placeholder="Enter the reason for closing...", 
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        thread = interaction.channel
        if not isinstance(thread, discord.Thread):
            await interaction.response.send_message(
                "This command can only be used in ticket threads.", ephemeral=True
            )
            return

                                           
        await interaction.response.defer(ephemeral=True)

                                                    
        db_connection = await get_database_connection()
        ticket_updated = False

        if db_connection:
            try:
                async with db_connection.cursor() as cursor:
                    await cursor.execute(
                        "UPDATE tickets SET status='closed', close_reason=%s WHERE channel_id = %s",
                        (self.reason.value, thread.id)
                    )
                    await db_connection.commit()
                    ticket_updated = True
            except Exception as e:
                logger.exception("Database error while updating ticket close reason")
            finally:
                db_connection.close()

                                                    
        await interaction.followup.send(
            "Are you sure you want to close this ticket?",
            ephemeral=True,
            view=CloseConfirmationView(reason=self.reason.value)
        )
