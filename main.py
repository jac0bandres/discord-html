import yaml
import discord
from discord.ext import commands
import sys
import os
from io import BytesIO
import asyncio
from dotenv import load_dotenv
from discord_html.parse import md_to_html
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")# Replace with your target channel ID

DEFAULT_CONFIG_PATH = "config.yaml"
config = {}

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="/", intents=intents)

def parse_command_args(flag_definitions, input_str):
    flags = input_str.strip().split()
    args = {}

    # Preload default values
    for flag in flag_definitions:
        name = flag["name"]
        arg_type = flag["type"]
        args[name] = False if arg_type == "bool" else None

    i = 0
    while i < len(flags):
        flag = flags[i]
        match = next((f for f in flag_definitions if f["name"] == flag), None)
        if not match:
            i += 1
            continue

        if match["type"] == "bool":
            args[flag] = True
            i += 1
        elif match["type"] == "string":
            if i + 1 < len(flags):
                args[flag] = flags[i + 1]
                i += 2
            else:
                raise ValueError(f"Expected value after {flag}")
        else:
            i += 1

    return args

@bot.command(name=config["parse_command_name"])
async def parse(ctx, args: str = config["args"]["default_args"]):
    """
    Convert Discord-style markdown to HTML.
    """

    if config["channels"]:
        if str(ctx.channel.id) not in map(str, config["channels"]):
            await ctx.send(f"This command can only be used in the following channels: {', '.join(config['channels'])}", ephemeral=True)
            return

    try:
        flags = args.split()
        parse_args = {
            "message_id": None,
            "file": None,
            "html": False,
            "markdown": False
        }
        if "--message-id" in flags:
            index = flags.index("--message-id")
            if index + 1 < len(flags):
                parse_args["message_id"] = flags[index + 1]
            else:
                return

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

def setup(config_path: str = "config.yaml"):
    """
    Setup function to initialize the bot.
    """
    if not TOKEN:
        raise ValueError("DISCORD_TOKEN environment variable not set.")
 
    with open(config_path, 'r') as f:
        if not f:
            raise ValueError(f"Config file {config_path} not found or is empty.")

        config = yaml.safe_load(f)
        
def main():
    """
    Main function to run the bot.
    """
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"An error occurred while running the bot: {str(e)}")

if __name__ == "__main__":
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    main()
