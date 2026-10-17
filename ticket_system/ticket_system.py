# -----------------------------------------------------------------------------
# File Name   : ticket_system.py
# Description : Registers the ticket-system cog, commands, and persistent ticket views.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               
                                                                               

import logging

import discord
from core.branding import attach_logo
from discord.ext import commands
from discord import app_commands
from ticket_system.ticket_views import TicketViewWrapper
from ticket_system.ticket_confirmation import CloseConfirmationView
from ticket_system.ticket_close import CloseTicketView
from ticket_system.ticket_add_user import AddUserToTicket
from ticket_system.ticket_remove_user import RemoveUserFromTicket
from ticket_system.close_request import CloseRequest
                                                         
from assets.mysql import get_database_connection
from utilities import TICKET_LOG_CHANNEL_ID, ALLOWED_CHANNEL_ID

logger = logging.getLogger(__name__)

class TicketSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        
        logger.info("Ticket system is ready")

    @app_commands.command(name="setupticket", description="Set up the ticket system with a select menu.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_ticket(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if interaction.channel.id != ALLOWED_CHANNEL_ID:
            await interaction.response.send_message(
                "This command cannot be used in this channel.", ephemeral=True
            )
            return

                               
        await interaction.response.defer(ephemeral=True)

        embed = discord.Embed(
            title="Garuda Cloud - Ticket System",
            description=(
                "\n**Network** | **Sales** | **Support**\n"
                "Click the related option below to create a ticket.\n\n"
                "**Network** - Report connectivity issues, server downtimes, or network-related queries.\n\n"
                "**Sales** - Inquire about services, pricing, or new purchases.\n\n"
                "**Support** - Get help with services or technical issues.\n\n"
                "**RULES TO FOLLOW**\n"
                "• Please be patient, our staff will assist you soon.\n"
                "• Answering the question is mandatory.\n"
                "• Please be respectful to moderators, we have the whole conversation recorded."
            ),
            color=discord.Color.purple()
        )
        embed.set_footer(text="Powered by Garuda Cloud")
        embed, logo_file = attach_logo(embed)

        await channel.send(embed=embed, view=TicketViewWrapper(self.bot), file=logo_file if logo_file else None)
        await interaction.followup.send(f"Ticket system set up in {channel.mention}!", ephemeral=True)

    @app_commands.command(name="closeticket", description="Close the current ticket thread.")
    @app_commands.describe(reason="Optional reason for closing the ticket.")
    async def close_ticket(self, interaction: discord.Interaction, reason: str = None):
        

        thread = interaction.channel
        if not isinstance(thread, discord.Thread):
            await interaction.response.send_message(
                "This command can only be used in ticket threads.", ephemeral=True
            )
            return

                               
        await interaction.response.defer(ephemeral=True)

        db_connection = await get_database_connection()
        ticket_id, user_id, category = None, None, None

        if db_connection:
            try:
                async with db_connection.cursor() as cursor:
                                             
                    await cursor.execute(
                        "SELECT ticket_number, user_id, category FROM tickets WHERE channel_id = %s",
                        (thread.id,)
                    )
                    result = await cursor.fetchone()

                    if not result:
                        await interaction.followup.send(
                            "This is not a valid ticket thread.", ephemeral=True
                        )
                        return

                    ticket_id, user_id, category = result

                                                                         
                    await cursor.execute(
                        "UPDATE tickets SET status='closed', close_reason=%s WHERE channel_id = %s",
                        (reason or "No reason specified", thread.id)
                    )
                    await db_connection.commit()

            except Exception as e:
                logger.exception("Database error while closing ticket")
                await interaction.followup.send("Error closing the ticket.", ephemeral=True)
                return
            finally:
                db_connection.close()

                                                       
        await interaction.followup.send(
            "Are you sure you want to close this ticket?",
            ephemeral=True,
            view=CloseConfirmationView(reason=reason or "No reason specified")
        )


async def setup(bot: commands.Bot):
    

    bot.add_view(TicketViewWrapper(bot))
    bot.add_view(CloseTicketView())
    await bot.add_cog(TicketSystem(bot))
    await bot.add_cog(AddUserToTicket(bot))
    await bot.add_cog(RemoveUserFromTicket(bot))
    await bot.add_cog(CloseRequest(bot))
                                           
