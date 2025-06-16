import discord
from discord.ext import commands
import os
from io import BytesIO
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
async def parse(ctx):
    """
    Convert Discord-style markdown to HTML.
    """
    result = dispatcher.dispatch("md_to_html", "**hello**")
    print(result)
    channel = ctx.channel
    message = ctx.message
    args_input = message.content.replace(conf["command_prefix"]+conf["command_name"],"").strip()

    if message.reference:
        message = await channel.fetch_message(message.reference.message_id)

    content = message.content
    args = bot_config.parse_input(flag_map=flag_map, input_str=args_input)  
    args.sort(key=lambda arg: arg['flag']['sequence'])
    print(args)
    for arg in args:
        if arg['flag']['sequence'] < 2:
            content = dispatcher.dispatch(arg['flag']['function'], content)

    await upload_content(content=content, content_type="html", ctx=ctx)



async def fetch_messages_by_id(ids: list[str], channel: discord.TextChannel):
    content = ""
    for id in ids:
        message = await channel.fetch_message(int(id))
        content += message.content

    return content

async def upload_content(content: str, content_type: str, ctx: commands.Context, file_name=''):
    file_name.replace(".html", "")
    if file_name == "":
        file_name = str(ctx.message.id)
    if content_type == "html":
        file_bytes = BytesIO(content.encode('utf-8'))

    await ctx.reply("HTML finished:", file=discord.File(file_bytes, filename=f"{str(ctx.message.id)}.html"))

bot.run(TOKEN)
