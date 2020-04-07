import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

team1 = []
team2 = []
maps = ["vertigo",  "dust2", "inferno", "nuke", "overpass", "cache", "cobblestone", "train"]

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="/")

@bot.event
async def on_ready():
    print(f"Connected to {bot.guilds[0].name}")

@bot.group(name="popflash", help="Start a popflash game")
async def popflash(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("/popflash start [cpt1] [cpt2] to start \n/popflash veto to start map veto")

@popflash.command(name="start", help="/popflash start [cpt1] [cpt2] to start a team pick")
async def start(ctx, cpt1: discord.User, cpt2: discord.User):
    team1.append(cpt1)
    team2.append(cpt2)
    await ctx.send(f"Popflash started, captain 1: {cpt1.mention}, captain 2: {cpt2.mention}")

    def check1(msg):
        return msg.author == cpt1 and len(msg.mentions) == 1

    def check2(msg):
        return msg.author == cpt2 and len(msg.mentions) == 1

    async def pick(cpt, check, team):
        await ctx.send(f"{cpt.mention}'s pick")
        player = await bot.wait_for("message", check=check)
        team.append(player.mentions[0])

    for i in range(4):
        await pick(cpt1, check1, team1)
        await pick(cpt2, check2, team2)
    nl = '\n - '
    await ctx.send(f"Team picks complete. /popflash veto to start map veto \n Team 1: \n - {nl.join([player.name for player in team1]) } \n \n Team 2: \n - {nl.join([player.name for player in team2])}")

@popflash.command(name="veto", help="Start a veto, if no teams have been chosen use '/popflash veto' for user who called command to control veto or '/popflash veto [cpt2]' to have two players control veto")
async def veto(ctx, *args: discord.User):
    global maps
    global team1
    global team2

    def check1(msg):
        return msg.author == team1[0] and msg.content in maps

    def check2(msg):
        return msg.author == team2[0] and msg.content in maps

    async def veto_map(maps, check, team):
        await ctx.send(f"Remaining maps: {', '.join(maps)} \n{team[0].mention}'s veto" )
        vetoed_map = await bot.wait_for("message", check=check)
        return list(filter(lambda x: x != vetoed_map.content.lower(), maps))

    if not team1 or not team2:
        team1 = [ctx.message.author]
        if args:
            team2 = [args[0]]
            message = f"Veto started without teams, **{ctx.message.author.name}** and **{args[0].name}** will control veto"
        else:
            team2 = team1
            message = f"Veto started without teams, **{ctx.message.author.name}** will control veto"
        await ctx.send(message)

    while len(maps) > 1:
        maps = await veto_map(maps, check1, team1)
        if len(maps) == 1:
            break
        maps = await veto_map(maps, check2, team2)
    await ctx.send(f"Chosen map: **{maps[0]}** \nhttps://popflash.site/scrim/connor")
    maps = ["vertigo",  "dust2", "inferno", "nuke", "overpass", "cache", "cobblestone", "train"]
    team1 = []
    team2 = []

bot.run(TOKEN)