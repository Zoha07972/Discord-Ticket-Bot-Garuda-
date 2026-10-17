# -----------------------------------------------------------------------------
# File Name   : ticket_views.py
# Description : Defines the persistent view displayed on the ticket creation panel.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               
                                                                               

import logging

import discord
from ticket_system.ticket_select import TicketSelect

logger = logging.getLogger(__name__)

class TicketViewWrapper(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(TicketSelect(bot))
