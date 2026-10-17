# -----------------------------------------------------------------------------
# File Name   : ticket_add_user.py
# Description : Provides the command for adding a member to a ticket thread.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               
                                                                               

import logging

import discord
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger(__name__)

class AddUserToTicket(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="adduserinticket", description="Add a user to the current ticket thread.")
    async def add_user(self, interaction: discord.Interaction, user: discord.Member):
        thread = interaction.channel
        
                                                    
        if not isinstance(thread, discord.Thread):
            await interaction.response.send_message("This command can only be used in ticket threads.", ephemeral=True)
            return

                                                    
        if user in thread.members:
            await interaction.response.send_message(f"{user.mention} is already a part of this ticket.", ephemeral=True)
            return
        
                                               
        try:
            await thread.add_user(user)

                          
            embed = discord.Embed(
                title="User Added to Ticket",
                description=f"{user.mention} has been added to {thread.mention}.",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Added by {interaction.user.display_name}", icon_url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to add users to this thread.", ephemeral=True)
        except Exception as e:
            logger.exception("Failed to add user to ticket thread")
            await interaction.response.send_message("An error occurred while adding the user.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(AddUserToTicket(bot))
