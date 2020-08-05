import discord
from discord.ext import commands
from discord.utils import get

import os
import json

from utils.welcomeInfo import WelcomeDB
from utils.gifInfo import GifDB
from utils.roleInfo import RoleDB


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome = None

    def cog_check(self, ctx):
        self.welcome = WelcomeDB(bot = self.bot, guild = ctx.guild)
        self.gif = GifDB(bot = self.bot, guild = ctx.guild)
        return True

    @commands.has_permissions(manage_messages = True)
    @commands.group(name = "welcome", invoke_without_command=True)
    async def welcome(self, ctx):
        embed = discord.Embed(description = "Choose which part of the welcome message you want to change: channel, message, gif. ", color = discord.Color.blue())
        await ctx.send(embed=embed)

    @welcome.command(name = "channel")
    async def channel(self, ctx, *, channel:discord.TextChannel):
        self.welcome.update_value(column = "channel", value=channel.id)
        embed = discord.Embed(description = f"Changed the welcome channel to {channel}", color = discord.Color.blue())
        await ctx.send(embed=embed)

    @welcome.command(name = "message")
    async def message (self, ctx, *, message = "Hi {mention} and welcome to {guild}"):
        self.welcome.update_value(column = "message", value = message)
        welcome_channel = self.welcome._get_welcome_channel()
        embed = discord.Embed(description = f"I will send {message} into {welcome_channel} whenever a new members joins the server!", color = discord.Color.blue())
        await ctx.send(embed=embed)

    @welcome.command(name="gif")
    async def gif (self, ctx, *, gif="https://thumbs.gfycat.com/AshamedAccomplishedIrishredandwhitesetter-small.gif"):
        self.gif.update_value(column="gif", value=gif)
        embed = discord.Embed(description=f"I will make sure to post this gif at the bottom of the welcome message", color = discord.Color.blue())
        embed.set_thumbnail(url=gif)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def autorole(self, ctx, *, res):
        role = RoleDB(bot=self.bot, guild = ctx.guild)
        try:
            autorole = get(ctx.guild.roles, name=res)
            role.update_value(column="bool", value=1)
            role.update_value(column="role", value=autorole)
            await ctx.send(f"Set {res} to the role that new members will get when they join")
        except Exception as e:
            await ctx.send("Error in adding role to auto role, either the role doesn't exist or the name is incorrect.")
            print(e)
    

def setup(bot):
    bot.add_cog(Welcome(bot))