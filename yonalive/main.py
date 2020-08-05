import discord
from discord.ext import commands
from discord.utils import get

from datetime import datetime

import os
import traceback
import json

from utils.welcomeInfo import WelcomeDB
from utils.prefixInfo import PrefixDB
from utils.roleInfo import RoleDB 
from utils.gifInfo import GifDB
from utils.leaveInfo import LeaveDB


config = json.load(open(os.getcwd()+'/config/config.json'))


def get_prefix (bot, message):
    prefix_db = PrefixDB(bot=bot, guild=message.guild)
    if not message.guild:
        return commands.when_mentioned_or("y-")(bot, message)
    
    prefix = prefix_db._get_prefix()
    return prefix


bot = commands.AutoShardedBot(command_prefix = get_prefix, case_insensitive=True)


bot.home_dir = os.getcwd()
bot.config = json.load(open('config/config.json'))
bot.token = bot.config["Bot"]["Token"]




initial_extensions = [
    "cogs.moderation",
    "cogs.meme",
    "cogs.misc",
    "cogs.personal",
    "cogs.prefix",
    "cogs.server",
    "cogs.leave"
]



if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}")
            traceback.print_exc()

@bot.event
async def on_message(message):
    prefix_db = PrefixDB(bot=bot, guild=message.guild)
    if f"<@!{bot.user.mention}" in message.content:
        if str(message.guild.id) in prefix_db._get_prefix():
            prefix = prefix_db._get_prefix()
        else:
            prefix = "y-"
        await message.channel.send(f"My prefix here is {prefix}")

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    print(f"Running on version {discord.__version__}")

@bot.event
async def on_member_join(member):
    welcome = WelcomeDB(bot = bot, guild = member.guild)
    gif = GifDB(bot=bot, guild = member.guild)
    role = RoleDB(bot=bot, guild = member.guild)
    raw_welcome_channel = welcome._get_welcome_channel()
    welcome_channel = bot.get_channel(raw_welcome_channel)
    welcome_message = welcome._get_welcome_message()

    welcome_gif = gif._get_gif()

    mention = member.mention
    user = member.name
    guild = member.guild

    rolebool = role._get_bool()
    if rolebool == 1:
        role1 = role._get_role()
        autorole = get(member.guild.roles, name = role1)
        await member.add_roles(autorole)


    embed = discord.Embed(color = discord.Color.blue(), description=str(welcome_message).format(mention=mention, user = user, guild = guild))
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
    embed.set_image(url=welcome_gif)
    embed.timestamp = datetime.utcnow()

    await welcome_channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    leave = LeaveDB(bot=bot, guild=member.guild)
    message = leave._get_message()
    channel = leave._get_channel()
    leave_channel = bot.get_channel(channel)
    
    mention = member.mention
    user = member.name
    guild = member.guild
    
    embed = discord.Embed(color = discord.Color.blue(), description=str(message).format(mention=mention, user = user, guild = guild))
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
    embed.timestamp = datetime.utcnow()

    await leave_channel.send(embed=embed)



@bot.command()
async def status(ctx, *, status):
    if ctx.author.id == 349256335742730253:
        await bot.change_presence(activity=discord.Game(name=status))
        await ctx.send(f"Changed Yona's status to {status}")




bot.run(bot.token)