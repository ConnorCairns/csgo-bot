import discord
from discord.ext import commands

class Popflash(commands.Cog):
    def __init__(self, bot, lobby_id: int, team1_id: int, team2_id: int):
        self.bot = bot
        self.team1 = []
        self.team2 = []
        self.maps = ["vertigo",  "dust2", "inferno", "nuke", "overpass", "cache", "cobblestone", "train", "mirage","anubis","chlorine"]
        self.stop = False
        self.lobby_id = lobby_id
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.lobby_channel = self.bot.get_channel(self.lobby_id)
        self.team1_channel = self.bot.get_channel(self.team1_id)
        self.team2_channel = self.bot.get_channel(self.team2_id)

    @commands.command(name="10man", help="/10man [cpt1] [cpt2] to start a team pick")
    async def start(self, ctx, cpt1: discord.User, cpt2: discord.User):
        self.stop = False
        self.team1.append(cpt1)
        self.team2.append(cpt2)
        await ctx.send(f"Popflash started, captain 1: {cpt1.mention}, captain 2: {cpt2.mention}")

        def check1(msg):
            return msg.author == cpt1 and len(msg.mentions) == 1 and msg.mentions[0] != self.bot.user

        def check2(msg):
            return msg.author == cpt2 and len(msg.mentions) == 1

        async def pick(cpt, check, team, team_channel, num):
            await ctx.send(f"{cpt.mention}'s pick ({4 - num} picks left)")
            player = await self.bot.wait_for("message", check=check)
            if player.mentions[0] in self.team1 or player.mentions[0] in self.team2:
                await ctx.send(f"{player.mentions[0].mention} is already in a team")
                await pick(cpt, check, team, num)
            else:
                team.append(player.mentions[0])
                #await player.mentions[0].move_to(team_channel)

        for i in range(1):
            if self.stop:
                break
            real_members = list(filter(lambda x: x.bot == False, self.lobby_channel.members))
            await ctx.send(f"Players not picked: {', '.join([member.mention for member in real_members])}")
            await pick(cpt1, check1, self.team1, self.team1_channel, i)
            if self.stop:
                break
            await ctx.send(f"Players not picked: {', '.join([member.mention for member in real_members])}")
            await pick(cpt2, check2, self.team2, self.team2_channel, i)
        nl = '\n - '
        if not self.stop:
            await ctx.send(f"Team picks complete. /veto to start map veto \n Team 1: \n - {nl.join([player.name for player in self.team1]) } \n \n Team 2: \n - {nl.join([player.name for player in self.team2])}")

    @commands.command(name="veto", help="Start a veto, if no teams have been chosen use '/popflash veto' for user who called command to control veto or '/popflash veto [cpt2]' to have two players control veto")
    async def veto(self, ctx, *args: discord.User):
        def check1(msg):
            return msg.author == self.team1[0] and msg.content in self.maps

        def check2(msg):
            return msg.author == self.team2[0] and msg.content in self.maps

        async def veto_map(maps, check, team):
            await ctx.send(f"Remaining maps: {', '.join(self.maps)} \n{team[0].mention}'s veto" )
            vetoed_map = await self.bot.wait_for("message", check=check)
            return list(filter(lambda x: x != vetoed_map.content.lower(), self.maps))

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
            self.maps = await veto_map(self.maps, check1, self.team1)
            if len(self.maps) == 1:
                break
            self.maps = await veto_map(self.maps, check2, self.team2)
        await ctx.send(f"Chosen map: **{self.maps[0]}** \nhttps://popflash.site/scrim/connor")
        self.maps = ["vertigo",  "dust2", "inferno", "nuke", "overpass", "cache", "cobblestone", "train"]
        self.team1 = []
        self.team2 = []

    # @commands.command(name="clear", help="Clear teams to start fresh")
    # async def clear(self, ctx):
    #     self.stop = True
    #     self.maps = ["vertigo",  "dust2", "inferno", "nuke", "overpass", "cache", "cobblestone", "train"]
    #     self.team1 = []
    #     self.team2 = []

def setup(bot):
    bot.add_cog(Popflash(bot, 158162147715710976, 695366273361510511, 695366328953077801))