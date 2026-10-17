# -----------------------------------------------------------------------------
# File Name   : ticket_close.py
# Description : Defines the ticket-close button and starts the confirmation workflow.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               
                                                                               

import logging

import discord
from discord.ext import commands                        
from ticket_system.ticket_confirmation import CloseConfirmationView
from ticket_system.ticket_modals import CloseReasonModal

logger = logging.getLogger(__name__)

class CloseTicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)                               

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

                                                               
        view = CloseConfirmationView(reason="No reason provided")  
        embed = discord.Embed(
            title="Ticket Close Confirmation",
            description="Are you sure you want to close this ticket?",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

    @discord.ui.button(label="Close with Reason", style=discord.ButtonStyle.grey, custom_id="close_ticket_reason")
    async def close_ticket_with_reason(self, interaction: discord.Interaction, button: discord.ui.Button):

        modal = CloseReasonModal()                                
        await interaction.response.send_modal(modal)

                                                      
async def setup(bot: commands.Bot):
    bot.add_view(CloseTicketView())                          
                                                                  
