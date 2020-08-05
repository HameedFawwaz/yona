import discord
from discord.ext import tasks, commands
from discord.utils import get
import asyncio

import json
import os

from utils.prefixInfo import PrefixDB


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.config = json.load(open(os.getcwd() + "/config/config.json"))
        self.bot = bot

    def cog_check(self, ctx):
        self.config = json.load(open(os.getcwd() + '/config/config.json'))
        return True

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def prefix(self, ctx, *, pre = "y-"):
        prefix_db = PrefixDB(bot = self.bot, guild = ctx.guild)
        prefix_db._create_new_prefix()
        prefix_db.update_value(column="prefix", pre=pre)
        await ctx.send(f"Changed the prefix to {pre}")


def setup(bot):
    bot.add_cog(Prefix(bot))