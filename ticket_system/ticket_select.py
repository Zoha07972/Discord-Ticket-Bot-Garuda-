# -----------------------------------------------------------------------------
# File Name   : ticket_select.py
# Description : Handles ticket category selection and creation of ticket threads.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               
                                                                               

import logging

import discord
from core.branding import attach_logo
from assets.mysql import get_database_connection
from ticket_system.ticket_close import CloseTicketView
from utilities import SUPPORT_ROLE_ID, SALES_ROLE_ID, NETWORK_ROLE_ID, GARUDA_ROLE_ID
import asyncio

logger = logging.getLogger(__name__)

CATEGORY_ROLES = {
    "Support": SUPPORT_ROLE_ID,
    "Sales": SALES_ROLE_ID,
    "Network": NETWORK_ROLE_ID,
}

class TicketViewWrapper(discord.ui.View):
    

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.add_item(TicketSelect(bot))

class TicketSelect(discord.ui.Select):
    

    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="Network", description="Report connectivity issues or downtime.", value="Network"),
            discord.SelectOption(label="Sales", description="Inquire about services, pricing, or purchases.", value="Sales"),
            discord.SelectOption(label="Support", description="Get help with services or technical issues.", value="Support"),
        ]
        super().__init__(placeholder="Select a ticket category...", options=options, custom_id="ticket_category_select")
        self.bot = bot

    async def get_next_ticket_number(self, cursor, guild_id):
        
        await cursor.execute("SELECT last_ticket_number FROM ticket_counter WHERE guild_id = %s", (guild_id,))
        result = await cursor.fetchone()
        next_ticket_number = (result[0] + 1) if result else 1

        if result:
            await cursor.execute("UPDATE ticket_counter SET last_ticket_number = %s WHERE guild_id = %s", (next_ticket_number, guild_id))
        else:
            await cursor.execute("INSERT INTO ticket_counter (guild_id, last_ticket_number) VALUES (%s, %s)", (guild_id, next_ticket_number))

        return next_ticket_number

    async def callback(self, interaction: discord.Interaction):
        
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        user = interaction.user
        ticket_channel = interaction.channel
        category = self.values[0]

        db_connection = await get_database_connection()
        if db_connection is None:
            await interaction.followup.send("Database connection failed.", ephemeral=True)
            return

        try:
            async with db_connection.cursor() as cursor:
                                                  
                await cursor.execute(
                    "SELECT channel_id FROM tickets WHERE guild_id = %s AND user_id = %s AND status = 'open'",
                    (guild.id, user.id)
                )
                existing_ticket = await cursor.fetchone()
                if existing_ticket:
                    existing_thread = guild.get_thread(existing_ticket[0])
                    if existing_thread:
                        await interaction.followup.send(f"You already have an open ticket: {existing_thread.mention}", ephemeral=True)
                        return

                                          
                next_ticket_number = await self.get_next_ticket_number(cursor, guild.id)
                thread_name = f"ticket-{next_ticket_number}"

                                        
            thread = await ticket_channel.create_thread(
                name=thread_name,
                type=discord.ChannelType.private_thread,
                invitable=False,
                auto_archive_duration=10080
            )

                                      
            await thread.add_user(user)

                                     
            role_id = CATEGORY_ROLES.get(category)
            role_mention = f"<@&{role_id}>" if role_id else ""
            garuda_mention = f"<@&{GARUDA_ROLE_ID}>"

                                 
            embed = discord.Embed(
                title=f"{category} Team",
                description="Thanks for contacting us! A staff member will be with you shortly.",
                color=discord.Color.green()
            )
            embed.set_footer(text="Powered by Garuda Cloud")
            embed, logo_file = attach_logo(embed)

                                                            
            if role_mention:
                tag_msg_task = asyncio.create_task(thread.send(f"{role_mention} {garuda_mention} A new ticket has been created."))
                async def delete_tag_message(task):
                    msg = await task
                    await msg.delete()
                asyncio.create_task(delete_tag_message(tag_msg_task))

            await thread.send(embed=embed, view=CloseTicketView(), file=logo_file if logo_file else None)

                                       
            async with db_connection.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO tickets (guild_id, user_id, channel_id, ticket_number, category, status) VALUES (%s, %s, %s, %s, %s, 'open')",
                    (guild.id, user.id, thread.id, next_ticket_number, category)
                )
                await db_connection.commit()

            await interaction.followup.send(f"Ticket created: {thread.mention}", ephemeral=True)

        except Exception as e:
            logger.exception("Ticket creation failed")
            await interaction.followup.send("Failed to create ticket.", ephemeral=True)
        finally:
            db_connection.close()
