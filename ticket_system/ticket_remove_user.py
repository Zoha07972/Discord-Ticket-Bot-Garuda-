# -----------------------------------------------------------------------------
# File Name   : ticket_remove_user.py
# Description : Provides the command for removing a member from a ticket thread.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               
                                                                               

import logging

import discord
from discord.ext import commands
from discord import app_commands
from utilities import SUPPORT_ROLE_ID, SALES_ROLE_ID, NETWORK_ROLE_ID, GARUDA_ROLE_ID

logger = logging.getLogger(__name__)

class RemoveUserFromTicket(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="removeticketuser", description="Remove a user from the current ticket thread.")
    @app_commands.describe(user="The user to remove from the ticket")
    async def remove_user(self, interaction: discord.Interaction, user: discord.Member):
        thread = interaction.channel
        
                                                     
        if not isinstance(thread, discord.Thread):
            await interaction.response.send_message("This command can only be used in a ticket thread.", ephemeral=True)
            return

                                                                  
        allowed_roles = {SUPPORT_ROLE_ID, SALES_ROLE_ID, NETWORK_ROLE_ID, GARUDA_ROLE_ID}
        if not any(role.id in allowed_roles for role in interaction.user.roles):
            await interaction.response.send_message("You do not have permission to remove users from tickets.", ephemeral=True)
            return

                                                   
        try:
            members = await thread.fetch_members()                                  
            member_ids = [member.id for member in members]                  
        except Exception as e:
            logger.exception("Failed to fetch ticket thread members")
            await interaction.response.send_message("Could not fetch thread members.", ephemeral=True)
            return

                                                    
        if user.id not in member_ids:
            await interaction.response.send_message(
                f"{user.mention} is not a member of this ticket thread. Please add them first.",
                ephemeral=True
            )
            return

                                     
        try:
            await thread.remove_user(user)
            embed = discord.Embed(
                title="User Removed from Ticket",
                description=f"{user.mention} has been removed from {thread.mention}.",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Action by {interaction.user.display_name}", 
                             icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to remove that user.", ephemeral=True)
        except Exception as e:
            logger.exception("Failed to remove user from ticket thread")
            await interaction.response.send_message("An error occurred while removing the user.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RemoveUserFromTicket(bot))
