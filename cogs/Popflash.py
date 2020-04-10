import discord
import os
import random
import math
from discord.ext import commands, tasks
from dotenv import load_dotenv

class Popflash(commands.Cog):
    def __init__(self, bot, lobby_id: int, team1_id: int, team2_id: int):
        self.bot = bot
        self.team1 = []
        self.team2 = []
        self.maps = ["vertigo",  "dust2", "inferno", "nuke", "overpass", "cache", "cobblestone", "train", "mirage","anubis","chlorine"]
        self.lobby_channel = self.bot.get_channel(lobby_id)
        self.team1_channel = self.bot.get_channel(team1_id)
        self.team2_channel = self.bot.get_channel(team2_id)

    def wrapper(self, cpt):
        def check(msg):
            return msg.author == cpt and len(msg.mentions) == 1 and msg.mentions[0] != self.bot.user
        return check

    async def pick(self, ctx, cpt, team, team_channel, num):
        await ctx.send(f"{cpt.mention}'s pick ({math.ceil(4 - (num / 2))} picks left)")
        player = await self.bot.wait_for("message", check=self.wrapper(cpt))
        if player.mentions[0] in self.team1 or player.mentions[0] in self.team2:
            await ctx.send(f"{player.mentions[0].mention} is already in a team")
            await self.pick(ctx, cpt, team, team_channel, num)
        else:
            team.append(player.mentions[0])
            try:
                await player.mentions[0].move_to(team_channel)
            except:
                await ctx.send("Player not connected to voice, could not move them")

    def get_remaining_players(self, cpt1, cpt2):
        remaining_players = list(filter(lambda x: x.bot == False, self.lobby_channel.members))
        try:
            remaining_players.remove(cpt1)
            remaining_players.remove(cpt2)
        except:
            pass #Only reason for failure is if captain has left lobby which is fine so no error handling needed
        return remaining_players

    @tasks.loop(count=8)
    async def pick_loop(self, ctx, cpt1, cpt2):
        real_members = self.get_remaining_players(cpt1, cpt2)
        await ctx.send(f"Players not picked: {', '.join([member.mention for member in real_members])}")
        if self.pick_loop.current_loop % 2 == 0:
            await self.pick(ctx, cpt1, self.team1, self.team1_channel, self.pick_loop.current_loop)
        else:
            await self.pick(ctx, cpt2, self.team2, self.team2_channel, self.pick_loop.current_loop)

    @commands.command(name="10man", help="/10man to start a team pick")
    async def start(self, ctx):
        if self.team1 or self.team2:
            self.reset()
            await ctx.send("Clearing previous teams")
        real_members = list(filter(lambda x: x.bot == False, self.lobby_channel.members))
        captains = random.sample(range(0,9),2)
        try:
            cpt1 = real_members[captains[0]]
            cpt2 = real_members[captains[1]]
        except:
            await ctx.send("Not enough people in lobby")
            return
        self.team1.append(cpt1)
        self.team2.append(cpt2)
        await ctx.send(f"Popflash started, captain 1: {cpt1.mention}, captain 2: {cpt2.mention}")
        await self.pick_loop.start(ctx, cpt1, cpt2)

        nl = '\n - '
        await ctx.send(f"Team picks complete. /veto to start map veto \n Team 1: \n - {nl.join([player.name for player in self.team1]) } \n \n Team 2: \n - {nl.join([player.name for player in self.team2])}")

    def veto_wrapper(self, team):
        def check(msg):
            return msg.author == team[0] and msg.content in self.maps
        return check

    @tasks.loop(count=1)
    async def veto_map(self, ctx, maps, team):
        await ctx.send(f"Remaining maps: {', '.join(self.maps)} \n{team[0].mention}'s veto" )
        vetoed_map = await self.bot.wait_for("message", check=self.veto_wrapper(team))
        self.maps = list(filter(lambda x: x != vetoed_map.content.lower(), self.maps))

    def reset(self):
        self.team1 = []
        self.team2 = []
        self.maps = ["vertigo",  "dust2", "inferno", "nuke", "overpass", "cache", "cobblestone", "train", "mirage","anubis","chlorine"]

    @commands.command(name="veto", help="Start a veto, if no teams have been chosen use '/veto' for user who called command to control veto or '/veto [cpt2]' to have two players control veto")
    async def veto(self, ctx, *args: discord.User):
        if not self.team1 or not self.team2:
            self.team1 = [ctx.message.author]
            if args:
                self.team2 = [args[0]]
                message = f"Veto started without teams, **{ctx.message.author.name}** and **{args[0].name}** will control veto"
            else:
                self.team2 = self.team1
                message = f"Veto started without teams, **{ctx.message.author.name}** will control veto"
            await ctx.send(message)

        while len(self.maps) > 1:
            await self.veto_map.start(ctx, self.maps, self.team1)
            if len(self.maps) == 1:
                break
            await self.veto_map.start(ctx, self.maps, self.team2)
        await ctx.send(f"Chosen map: **{self.maps[0]}** \nhttps://popflash.site/scrim/connor")
        self.reset()
        
    @commands.command(name="cancel", help="Cancel match")
    async def cancel(self, ctx):
        self.veto_map.cancel()
        self.pick_loop.cancel()
        self.reset()
        await ctx.send("Cancelled")

def setup(bot):
    load_dotenv()
    LOBBY_ID = int(os.getenv('LOBBY_ID'))
    TEAM1_ID = int(os.getenv('TEAM1_ID'))
    TEAM2_ID = int(os.getenv('TEAM2_ID'))
    bot.add_cog(Popflash(bot, LOBBY_ID, TEAM1_ID, TEAM2_ID))