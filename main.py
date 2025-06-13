import discord
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

client = discord.Client(intents=intents)

def discord_markdown_to_html(content: str) -> str:
    return f"<p>{content}</p>"

@client.event
async def on_ready():
    print("Bot logged in as", client.user)
    print("Listening for messages in channel ID:", TARGET_CHANNEL_ID)
    channel = client.get_channel(TARGET_CHANNEL_ID)
    if channel is None:
        print(f"Channel with ID {TARGET_CHANNEL_ID} not found.")
        return

    await channel.send("Bot is now online and ready to process messages!")


@client.event
async def on_message(message: discord.Message):
    print("Received a message", message.content)
    if message.author.bot:
        return

    if message.channel.id != int(TARGET_CHANNEL_ID):
        print(f"Ignored message from channel {message.channel.id}.")
        return

    html_content = parse.md_to_html(message.content)
    with open(f"{message.id}.html", "a", encoding="utf-8") as f:
        f.write(html_content)

client.run(TOKEN)
