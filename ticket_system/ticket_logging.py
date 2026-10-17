# -----------------------------------------------------------------------------
# File Name   : ticket_logging.py
# Description : Sends ticket closure details to the configured staff log channel.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               
                                                                               

import logging

import discord
from datetime import datetime
import pytz
from utilities import TICKET_LOG_CHANNEL_ID

logger = logging.getLogger(__name__)

IST = pytz.timezone("Asia/Kolkata")

async def log_ticket_close(interaction: discord.Interaction, ticket_id, opened_by, claimed_by, open_time, reason, thread, transcript_file):
    
    
    close_time_formatted = datetime.now(IST).strftime("%d %B %Y at %I:%M %p")
    guild_id = interaction.guild.id
    ticket_url = f"https://discord.com/channels/{guild_id}/{thread.id}"

                              
    embed = discord.Embed(
        title="Ticket Closed",
        color=discord.Color.red(),
    )
    embed.add_field(name="**Ticket ID**", value=f"`{ticket_id or 'Unknown'}`", inline=True)
    embed.add_field(name="**Opened By**", value=opened_by, inline=True)
    embed.add_field(name="**Closed By**", value=interaction.user.mention, inline=True)
    embed.add_field(name="**Open Time**", value=open_time, inline=True)
    embed.add_field(name="**Claimed By**", value=claimed_by, inline=True)
    embed.add_field(name="**Reason**", value=reason, inline=True)
    embed.set_footer(text=f"Closed at {close_time_formatted}")

                             
    view = discord.ui.View()
    reopen_button = discord.ui.Button(label="View Ticket", url=ticket_url, style=discord.ButtonStyle.link)
    view.add_item(reopen_button)

                                                                 
    log_channel = interaction.guild.get_channel(TICKET_LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed, view=view)

                                                                            
    if opened_by:
        try:
            opened_by_user = interaction.guild.get_member(int(opened_by.strip("<@!>")))
            if opened_by_user:
                await opened_by_user.send(embed=embed, view=view)
        except discord.Forbidden:
            logger.warning("Could not DM ticket owner %s; DMs may be disabled", opened_by)
