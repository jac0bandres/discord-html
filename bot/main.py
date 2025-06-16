import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
import discord_html
import dispatcher
import bot_config
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")# Replace with your target channel ID

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.guild_messages = True  # Enable guild messages intent
conf = bot_config.open_config_file()
flag_map = bot_config.get_flags(conf["args"]["parse"])

bot = commands.Bot(command_prefix=conf["command_prefix"], intents=intents)

# TODO: parse based on message magic string instead of explicit command call

@bot.command(name=conf["command_name"])
async def parse(ctx, args: str = conf["default_args"]):
    """
    Convert Discord-style markdown to HTML.
    """
    content = "**HELLO**" # TODO: grab content from reference
    try:
        args = bot_config.parse_input(flag_map=flag_map, input_str=args)  
        if "--html" in args and args["--html"] == True:
            content = dispatcher.dispatch("md_to_html", content)
       # if "--md" in args and args["md"] == True:
       #     content = dispatcher.dispatch("md_to_html", content)
        print(content)

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

bot.run(TOKEN)
