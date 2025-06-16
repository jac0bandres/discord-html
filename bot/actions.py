from io import BytesIO
import discord  
import discord.ext

async def fetch_messages_by_id(ids: list[str], channel: discord.TextChannel):
    content = ""
    for id in ids:
        message = await channel.fetch_message(int(id))
        content += message.content

    return content
