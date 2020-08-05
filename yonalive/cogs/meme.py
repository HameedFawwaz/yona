import discord 
from discord.ext import tasks, commands
from discord.utils import get

import json
import os

import time
from datetime import datetime
import asyncio


class Meme(commands.Cog):
    def __init__(self, bot):
        self.config = json.load(open(os.getcwd() + "/config/config.json"))
        self.bot = bot
    
    def cog_check(self, ctx):
        self.config = json.load(open(os.getcwd() + '/config/config.json'))
        return True

    @commands.command(name = "Fuck", help="Insults a user", usage="fuck {user}")
    async def fuck(self, ctx, member):
        await ctx.send(f"{member} is an absolute retard. :middle_finger: Fuck you ")

    @commands.command()
    async def gay(self, ctx, member: discord.Member):
        await ctx.send(f"{member.mention} is now sucking your cock, what a fag. ")


def setup(bot):
    bot.add_cog(Meme(bot))