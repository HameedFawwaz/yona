import discord 
from discord.ext import tasks, commands
from discord.utils import get

import json
import os
import random

import time
from datetime import datetime
import asyncio
import aiohttp


class Misc(commands.Cog):
    def __init__(self, bot):
        self.config = json.load(open(os.getcwd() + "/config/config.json"))
        self.bot = bot


    def cog_check(self, ctx):
        return True


    @commands.command(name = "Ping")
    async def ping(self, ctx):
        ping_ = self.bot.latency
        ping = round(ping_ * 1000)
        await ctx.send(f"my ping is **{ping} ms**")
        print(f"my ping is {ping} ms")


    @commands.command()
    async def shutthefuckup(self, ctx, member: discord.Member):
        userid = ctx.message.author.id 

        if userid == 448649939082412032:
            await ctx.send("Shut the fuck up before I mute ur ass")
            mute_role = get(member.guild.roles, name = 'Muted')
            await member.add_roles(mute_role)
        else:
            await ctx.send("Nice try fuck tard, you can't do that. ")


    @commands.command(name="Marry", help="Gives the chance that you will marry a user", usage="Marry {user}")
    async def marry(self, ctx, member):
        for x in range(1):
            x = random.randint(41, 101)
            await ctx.send(f"{ctx.author.mention} has a {x}% chance of getting with {member}")

            print(f"{ctx.author.name} asked out {member}")


            if x > 50:
                print(f"{ctx.author.name} has a decent chance at winning over {member}")
                await ctx.send(f"{ctx.author.name} has a decent chance at winning over {member}")
            else:
                print(f"{ctx.author.name} is bouta get rejected lmfao")
                await ctx.send(f"{ctx.author.name} is bouta get rejected lmfao")
            break


    @commands.command(name="RNG", help="Generates a random number, default value is 1 100", usage="rng {number 1} {number 2}")
    async def rng(self, ctx, range1 = 1, range2 = 101):
        await ctx.send(random.randint(range1, range2))

    @commands.command(name="RPS", help="Plays Rock Paper Scissors with Yona", usage="rps (choice)")
    async def rps(self, ctx, choice = "rock"):
        raw_botchoice = ["rock", "paper", "scissors"]
        botchoice = raw_botchoice[random.randint(0, 2)]

        if botchoice == choice:
            await ctx.send(f"We both chose {botchoice}, it is a tie!")
        elif choice == "rock":
            if botchoice == "paper":
                await ctx.send("I chose paper, I win!")
            else:
                await ctx.send(f"I chose {botchoice}, {ctx.author.name} wins!")
        elif choice == "paper":
            if botchoice == "scissors":
                await ctx.send("I chose scissors, I win!")
            else:
                await ctx.send(f"I chose {botchoice}, {ctx.author.name} wins!")
        elif choice == "scissors":
            if botchoice == "rock":
                await ctx.send("I chose rock, I win!")
            else:
                await ctx.send(f"I chose {botchoice}, {ctx.author.name} wins!")


    @commands.command(name="MemberCount", help="Shows you the number of members in the server", usage="membercount")
    async def membercount(self, ctx):
        await ctx.send(f"**{ctx.guild.name}** has **{ctx.guild.member_count} members**")
        
def setup(bot):
    bot.add_cog(Misc(bot))