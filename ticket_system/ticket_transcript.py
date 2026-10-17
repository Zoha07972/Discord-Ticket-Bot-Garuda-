# -----------------------------------------------------------------------------
# File Name   : ticket_transcript.py
# Description : Generates and saves text transcripts of ticket conversations.
#
# Author      : X
# Created On  : Original creation date not recorded
# Last Updated: 17/10/2026
# -----------------------------------------------------------------------------                                                                               
                                                                               

import logging

import discord
import aiofiles
import os
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)

IST = pytz.timezone("Asia/Kolkata")

async def generate_transcript(thread: discord.Thread):
    
    
    messages = [msg async for msg in thread.history(limit=None, oldest_first=True)]

    if not messages:
        return None                       

    transcript_filename = f"transcripts/{thread.name}_{datetime.now(IST).strftime('%Y-%m-%d_%I-%M-%p')}.txt"
    os.makedirs("transcripts", exist_ok=True)                                   

    async with aiofiles.open(transcript_filename, "w", encoding="utf-8") as f:
        for message in messages:
            timestamp = message.created_at.astimezone(IST).strftime("%Y-%m-%d %I:%M %p")
            author = message.author.display_name
            await f.write(f"[{timestamp}] {author}: {message.content}\n")

    return transcript_filename                                        
