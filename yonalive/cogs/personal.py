import discord 
from discord.ext import tasks, commands
from discord.utils import get

import json
import os
import random

import time
from datetime import datetime
import asyncio


class Personal(commands.Cog):
    def __init__(self, bot):
        self.config = json.load(open(os.getcwd() + "/config/config.json"))
        self.bot = bot

    def cog_check(self, ctx):
        self.config = json.load(open(os.getcwd() + '/config/config.json'))
        return True

    @commands.command(pass_context = True, aliases = ["j", "joi"])
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await ctx.send(f"Joined {channel}")



    @commands.command(pass_context = True, aliases = ["l", "lea"])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        
        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"Bot has left {channel}")
            await ctx.send(f"Left {channel}")
        else:
            print("Bot was told to leave voice channel, but was not in one")
            await ctx.send("Wow, you really think that I'm in a voice channel do you?")


    @commands.command()
    async def china(self, ctx):
        userid = ctx.author.id

        if userid == 349256335742730253:

            voice = get(self.bot.voice_clients, guild = ctx.guild)

            voice.play(discord.FFmpegPCMAudio("alex.mp3"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
            
            
            await ctx.send(f"American Luigi is now Chinese Luigi")

        else:
            await ctx.send("That wasn't very Xie Wua Piao Piao of you. ")

    @commands.command()
    async def bullysaki1(self, ctx):
        saki = ctx.guild.get_member(337806367698190336)

        await ctx.send(f"{saki.mention} make the boys a sandwhich you whore, here are the ingredients now, hurry the fuck up. https://cdn.discordapp.com/attachments/496127351130947585/731257991839481926/Sandwhich_2.jpg")

    @commands.command()
    async def bullysaki2(self, ctx):
        saki = ctx.guild.get_member(337806367698190336)

        await ctx.send(f"{saki.mention} hey bitch, I just shit my pants, go do the laundry. https://cdn.discordapp.com/attachments/496127351130947585/731259097600753724/Laundry.png")

    @commands.command()
    async def bullysaki3(self, ctx):
        saki = ctx.guild.get_member(337806367698190336)

        await ctx.send(f"{saki.mention} hey you lazy dishwasher, start doing the fucking dishes. https://cdn.discordapp.com/attachments/496127351130947585/731259120606249090/dishes-20111117-101830.jpg")

    
    @commands.command()
    async def bruh(self, ctx, member: discord.Member):
        userid = ctx.message.author.id 

        if userid == 379128692674134016:
            await ctx.send(f"{member.mention} is an absolute clown lol :clown: :clown: :clown:")
        else:
            await ctx.send("Nice try bitch")

    @commands.command()
    async def pog(self, ctx):
        embed = discord.Embed(color = discord.Color.purple())
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/714129248843202580.png?v=1")
        await ctx.send(embed=embed)

    @commands.command()
    async def fuckrara(self, ctx):
        if ctx.author.id == 349256335742730253:
            rara = ctx.guild.get_member(567916026566541333)
            await rara.send("You said I wouldn't make this command, smh u were very wrong")
            while True:
                await rara.send("lmfao, imagine betting that I wouldn't make a bully command lmfao")



def setup(bot):
    bot.add_cog(Personal(bot))