# -----------------------------------------------------------------------------
# File Name   : ticket_confirmation.py
# Description : Confirms ticket closure and coordinates transcript and closure logging.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               
                                                                               

import logging

import discord
from ticket_system.ticket_transcript import generate_transcript
from ticket_system.ticket_logging import log_ticket_close
from assets.mysql import get_database_connection

logger = logging.getLogger(__name__)

class CloseConfirmationView(discord.ui.View):
    
    
    def __init__(self, reason: str):
        super().__init__(timeout=None)                   
        self.reason = reason

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="confirm_close_yes")
    async def confirm_close_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
       
        thread = interaction.channel
        if not isinstance(thread, discord.Thread):
            await interaction.response.send_message(
                "This command can only be used in ticket threads.",
                ephemeral=True
            )
            return

                                                                                    
        await interaction.response.defer(ephemeral=True)

                                  
        transcript_file = await generate_transcript(thread)
        logger.info("Ticket transcript generated: %s", transcript_file)

                               
        db_connection = await get_database_connection()
        ticket_id, opened_by, claimed_by, open_time = None, None, None, None

        if db_connection:
            try:
                async with db_connection.cursor() as cursor:
                    await cursor.execute("""
                        SELECT ticket_number, user_id, claimed_by, created_at
                        FROM tickets WHERE channel_id = %s
                    """, (thread.id,))
                    ticket_data = await cursor.fetchone()

                    if ticket_data:
                        ticket_id, opened_by, claimed_by, open_time = ticket_data
                        opened_by = f"<@{opened_by}>" if opened_by else "Unknown"
                        claimed_by = f"<@{claimed_by}>" if claimed_by else "Not claimed"
                        open_time = open_time.strftime("%d %B %Y at %I:%M %p") if open_time else "Unknown"

                               
                    await cursor.execute("UPDATE tickets SET status='closed' WHERE channel_id = %s", (thread.id,))
                    await db_connection.commit()
                    logger.info("Ticket %s status updated to closed", ticket_id)
            except Exception as e:
                logger.exception("Database error while closing ticket")
            finally:
                db_connection.close()

                          
        try:
            if not thread.archived:
                await interaction.followup.send("Ticket has been closed successfully.", ephemeral=False)
                await thread.edit(archived=True, locked=True)
                logger.info("Ticket thread %s locked and archived", thread.id)
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to archive or lock this thread!", ephemeral=True)
            return
        except Exception as e:
            await interaction.followup.send(f"Error locking/archiving thread: {e}", ephemeral=True)
            return

                         
        await log_ticket_close(interaction, ticket_id, opened_by, claimed_by, open_time, self.reason, thread, transcript_file)

    @discord.ui.button(label="No", style=discord.ButtonStyle.grey, custom_id="confirm_close_no")
    async def confirm_close_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        
                                                          
        if not interaction.response.is_done():
            await interaction.response.send_message("Ticket closure cancelled.", ephemeral=True)
        else:
            await interaction.followup.send("Ticket closure cancelled.", ephemeral=True)
