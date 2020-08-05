import discord
from discord.ext import commands

import os
import json




class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return True

    
    @commands.command(name='help')
    async def help(self, ctx):
        await ctx.send("Sent the help message into your DM")
        embed = discord.Embed(title="List of all of the help commands", description="""List of all the help command categories, react to this message to go to specific pages
Moderation: :desktop:
Server Customization: :printer: 
Meme: :rofl: 
Misc: :star: """, color = discord.Color.purple())

        msg = await ctx.author.send(embed = embed)
        await msg.add_reaction("🖥️")
        await msg.add_reaction("🖨️")
        await msg.add_reaction("🤣")
        await msg.add_reaction("🌟")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not isinstance(reaction.message.channel, discord.DMChannel):
            return
        if isinstance(reaction.message.channel, discord.DMChannel):
            users = await reaction.users().flatten()
            for bot in users:
                if bot == reaction.message.author:
                    print("Bot reacted")
                if bot != reaction.message.author:
                    if reaction.emoji == '🖥️':
                        channel = reaction.message.channel
                        embed = discord.Embed(title = "Help Command: Moderation", description = """
                **clear**: (amount): Deletes a set amount of messages, default value is 2
                **purge**: Deletes all messages in the channel
                **ban** (user): permanently bans a user from the server
                **unban** (user): Unbans a user from the server
                **kick** (user): Kicks a user from the server
                **slowmode** (time): activates slowmode for a channel, 0 is to turn off, 5 seconds is the default value. (Enter the value without s at the end)
                **mute** (time): Mutes user for a certain amount of time, the time is in hours.
                **warn** (user) (reason): Warns a user for a reason.
                **warnings** (user): displays the current warnings that a specific user has. 
                **removewarn** (user) (id): removes a warning from the user, the id of the warning can be found with the warnings command. """, color = discord.Color.purple())
                        await channel.send(embed=embed)
                    if reaction.emoji == '🖨️':
                        channel = reaction.message.channel
                        embed = discord.Embed(title = "Help Command: Server Management", description = """
                **welcome**: With this command, you need to choose which part of the welcome message you are trying to change, channel, message, gif.
                **prefix** (prefix): Choose the server's prefix, default value is y-.
                **autorole** (role): Adds role to new members when they join.""", color = discord.Color.purple())
                        await channel.send(embed=embed)
                    if reaction.emoji == '🤣':
                        channel = reaction.message.channel
                        embed = discord.Embed(title = "Help Command: Meme", description = """
                **fuck** (user): Insults a user that you put in""", color = discord.Color.purple())
                        await channel.send(embed=embed)
                    if reaction.emoji == '🌟':
                        channel = reaction.message.channel
                        embed = discord.Embed(title = "Help Command: Misc", description = """
                **afk** (time) (status): Sets your AFK status
                **marry** (user): You are tested to see if you are compatible with the other user""", color = discord.Color.purple())
                        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))