import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
import parser.parse as parse
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")# Replace with your target channel ID

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.guild_messages = True  # Enable guild messages intent

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.command(name='parse')
async def parse(ctx, *, args: str ="--html"):
    """
    Convert Discord-style markdown to HTML.
    """
    try:
        if ctx.message.reference:
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            html_content = parse.md_to_html(replied_message.content)
            print(html_content)
        #await ctx.send(html_content) 
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

bot.run(TOKEN)
