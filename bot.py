import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="/")
cogs = ['cogs.Popflash']

@bot.event
async def on_ready():
    print(f"Connected to {bot.guilds[0].name}")
    for cog in cogs:
        bot.load_extension(cog)
    return

@bot.command(name="reload", help="Reload all cogs to start fresh")
async def reload(ctx):
    for cog in cogs:
        bot.reload_extension(cog)
        await ctx.send(f"Reloaded {cog}")

bot.run(TOKEN)