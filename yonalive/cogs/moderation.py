import discord
from discord.ext import tasks, commands
from discord.utils import get
import asyncio

import json
import os

from utils.warningInfo import Warning


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.config = json.load(open(os.getcwd() + "/config/config.json"))
        self.bot = bot

    def cog_check(self, ctx):
        self.config = json.load(open(os.getcwd() + '/config/config.json'))
        return True

    @commands.command(name="Clear", help="Deletes a certain amount of messages", usage="clear {amount}")
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=int(amount))
        user = ctx.author.name
        print(f"{user} deleted {amount} messages. ")


    @commands.command(name="Purge", help="Removes all messages in a channel, if you pass a value, it will also delete that amount", usage="purge {amount} (amount is optional)")
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount=100000000):
        await ctx.channel.purge(limit=int(amount))
        user = ctx.author.name
        print(f"{user} has purged a channel")

    @commands.command(name="Ban", help="Bans member from server", usage="ban {user} {reason}")
    @commands.has_permissions(ban_members = True)
    async def ban (self, ctx, member: discord.Member, *, reason = None):
        await member.ban(reason = reason)
        await ctx.send(f"{member} has been banned")
        banned_user = member

        print(f"{ctx.author.name} banned {banned_user}. ")

    @commands.command(name="Unban", help="Unbans a member from server", usage="unban {user}")
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.name}#{user.discriminator}")


    @commands.group(name = "slowmode")
    @commands.has_permissions(manage_channels = True)
    async def slowmode(self, ctx, *, response):
        if type(response) == str:
            if response == "off":
                await ctx.channel.edit(slowmode_delay=0)
                await ctx.send("Slowmode in this channel has been removed.")
            else:
                res = response[:-1]
                if res == '':
                    await ctx.channel.edit(slowmode_delay=int(response))
                    await ctx.send(f"Slowing down this channel by {response}s")
                else:
                    await ctx.channel.edit(slowmode_delay=int(res))
                    await ctx.send(f"Slowing down this channel by {response}")
        else:
            await ctx.send(f"Invalid Value, Try Again. ")



    @slowmode.command(name = 'off')
    async def slowmode_off(self, ctx, response: str):
        await ctx.channel.edit(slowmode_delay = 0)
        await ctx.send("Turning off slowmode in this channel")
        print(f"{ctx.author.name} has turned off slowmode in {ctx.channel.name}")

    @commands.command(name = "Warn", help="Warns member in server", usage="warn {user} {reason}")
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, users: commands.Greedy[discord.Member], *, reason = "No reason provided"):
        warned_users = []
        for user in users:
            userWarns = Warning(bot=self.bot, ctx=ctx, user=user)
            userWarns.warn(reason)
            warned_users.append(user.name)
        embed = discord.Embed(title=f"Warned users", color=discord.Color.orange())
        embed.add_field(name=f"Warned {len(warned_users)} user(s)", value="\n".join(warned_users))
        embed.set_footer(text=reason)
        await ctx.send(embed=embed)

    @commands.command(name="Warnings", help="Checks the current warnings for a user", usage="warnings {user}")
    @commands.has_permissions(manage_guild=True)
    async def warnings (self, ctx, user: discord.Member = None):
        if not user: 
            user = ctx.author
        userWarns = Warning(bot = self.bot, ctx=ctx, user=user)
        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name=f"{user.name}'s Warnings", value="\n".join([f"{int(index) + 1}: {warn}" for index, warn in userWarns.warns.items()]) if userWarns.warns else "None")
        await ctx.send(embed=embed)

    @commands.command(name="RemoveWarn", help="Removes a warning from a user, the id can be found by using warnings", usage="removewarn {user} {id}")
    @commands.has_permissions(manage_guild=True)
    async def removewarn (self, ctx, user: discord.Member, warn_id: int):
        userWarns = Warning(bot = self.bot, ctx=ctx, user=user)
        userWarns.remove(warn_id-1)
        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name=f"{user.name}'s Warnings", value="\n".join([f"{int(index) + 1}: {warn}" for index, warn in userWarns.warns.items()]) if userWarns.warns else "None")
        embed.set_footer(text="Removed a warning, here is the users current warnings")
        await ctx.send(embed=embed)

    @commands.command(name="Kick", help="Kicks a user from the server", usage="kick {user} {reason}")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked")
        user = ctx.author.name
        print(f"{user} has banned {member}")

    @commands.command(name="Mute", help="Mutes a user for 1h", usage = "mute {time} {reason}")
    @commands.has_permissions(manage_roles = True)
    async def mute (self, ctx, member: discord.Member, time = 1, reason = 'None'):
        mute_role = get(member.guild.roles, name = 'Muted')
        await member.add_roles(mute_role, reason = reason)
        print(f"{ctx.author} muted {member.mention} for {time} hour(s)")
        await ctx.send(f"Muted {member} for {time} hour()")

        if time > 0:
            await asyncio.sleep(time * 3600)
            await member.remove_roles(mute_role, reason = "Times up")
            await ctx.send(f"Time's up {member.mention} your prison sentence is over with. ")
            print(f"{member} has been unmuted due to the timer running out.")


    @commands.command(name="Unmute", help="Removes the mute off of a user", usage="unmute {user}")
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, member: discord.Member):
        await ctx.send(f"{member.mention} has been unmuted")
        mute_role = get(member.guild.roles, name = 'Muted')
        await member.remove_roles(mute_role)
        print(f"{ctx.author.name} unmuted {member}")

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def lockdown(self, ctx, response):
        if response == "channel":
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
            await ctx.send(f"This channel has been locked down")
            print(f"This channel has been locked down")
        elif response == "off":
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)
            await ctx.send("Removed the lockdown")
        else:
            await ctx.send("Please enter either channel to activate a lockdown in the current channel or off to remove the lockdown in the current channel. ")
            await ctx.send("Lockdown removed")

def setup(bot):
    bot.add_cog(Moderation(bot))