import discord
from discord.ext import tasks, commands
import asyncio
import time
from datetime import datetime
import random
import aiohttp
from discord.utils import get

def read_token():
    with open("token.txt", "r") as f:
        liens = f.readlines()
        return liens[0].strip()

with open ("reports.json", encoding='utf-8') as f:
    try:
        report = json.load(f)
    except ValueError:
        report = {}
        report['users'] = []


bot = commands.Bot(command_prefix = 'y-', case_insensitive=True)
token = read_token()
messages = joined = 0


now = datetime.now()
current_time = now.strftime("%H:%M")
#-----INDICATOR FOR BOT READY-----

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    print(f"Running on version {discord.__version__}")



#-----STATS FOR SERVER-----
async def update_stats():
    await bot.wait_until_ready()
    global messages, joined

    while not bot.is_closed():
        try:
            with open ("stats.txt", 'a') as s:
                s.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")
            
            messages = 0
            joined = 0

            await asyncio.sleep(86400)
        except Exception as e:
            print(e)


#-----BOT WELCOME MESSAGE-----

@bot.event
async def on_member_join(member):
    global joined
    joined += 1
    """with open('warns.json', 'r') as f:
        users = json.load(f)"""
    channel = bot.get_channel(712508604770418692)
    rules_channel = bot.get_channel(712516237028229172)
    await channel.send(f"what’s good {member.mention}, welcome to :shinto_shrine:**Kenkyona Village** :shinto_shrine:! Make sure to read {rules_channel.mention} have a chill time with us!")
    print(f"{current_time} - {member} has joined the server. ")

#----------MODERATION-------------
@bot.event
async def on_message(message):
    global messages
    messages += 1

    if message.content.lower() == 'nigger':
        user = message.author.name
        await message.delete()
        await message.channel.send(f"{user} has dropped a hard r")
        await message.author.ban(reason = "User dropped a hard r")
        print(f"{current_time} - {user} has been banned for dropping a hard r. ")

    await bot.process_commands(message)


@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=int(amount))
    user = ctx.author.name
    print(f"{current_time} - {user} deleted {amount} messages. ")

@bot.command()
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount=100000000):
    await ctx.channel.purge(limit=int(amount))
    user = ctx.author.name
    print(f"{current_time} - {user} has purged a channel")

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban (ctx, member: discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f"{member} has been banned")
    banned_user = member
    print(f"{current_time} - {ctx.author.name} banned {banned_user}. ")

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, userId):
    user = discord.Object(id=userId)
    await ctx.guild.unban(user)
    await ctx.send(f"Unbanned {user}")


@bot.group(name = "slowmode")
@commands.has_permissions(manage_channels = True)
async def slowmode(ctx, response: int):
    await ctx.channel.edit(slowmode_delay=response)
    await ctx.send(f"Slowing down this channel by {response}s")
    print(f"{current_time} - {ctx.author.name} has slowed down {ctx.channel.name} by {response}s")


@slowmode.command(name = 'off')
async def slowmode_off(ctx, response: str):
    await ctx.channel.edit(slowmode_delay = 0)
    await ctx.send("Turning off slowmode in this channel")
    print(f"{current_time} - {ctx.author.name} has turned off slowmode in {ctx.channel.name}")

'''

@bot.command()
@commands.has_permissions(manage_roles=True, ban_members = True)
async def warn (ctx, member: discord.member, *reason:str):
    if not reason:
        await ctx.send("Please provide a reason")
        return
    reason = ' '.join(reason)
    for current_user in report['users']:
        if current_user['name'] == member.name:
            current_user['reasons'].append(reason)
            break
        else:
            report['users'].append({
                'name':member.name,
                'reasons': [reason]
            })
    with open ('reports.json' ,'wt') as f:
        json.dump(report, f)

@bot.command()
async def warnings (ctx, member:discord.Member):
    for current_user in report['users']:
        if member.name == current_user['users']:
            await ctx.send("{member.name} has been reported {len(current_user['reasons'])} times : {",".join(current_user['reasons'])}")
        else:
            await ctx.send(f"{member.name} has never been reported")


'''

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked")
    user = ctx.author.name
    print(f"{current_time} - {user} has banned {member}")

@bot.command()
@commands.has_permissions(manage_roles = True)
async def mute (ctx, member: discord.Member, time: int, reason = 'None'):
    mute_role = get(member.guild.roles, name = 'Muted')
    await member.add_roles(mute_role, reason = reason)
    print(f"{current_time} - {ctx.author} muted {member.mention} for {time} minute(s)")
    await ctx.send(f"Muted {member} for {time} minute(s)")

    if time > 0:
        await asyncio.sleep(time * 60)
        await member.remove_roles(mute_role, reason = "Times up")
        await ctx.send(f"Time's up {member.mention} your prison sentence is over with. ")
        print(f"{current_time} - {member} has been unmuted due to the timer running out.")


@bot.command()
@commands.has_permissions(manage_roles = True)
async def unmute(ctx, member: discord.Member):
    await ctx.send(f"{member.mention} has been unmuted")
    mute_role = get(member.guild.roles, name = 'Muted')
    await member.remove_roles(mute_role)
    print(f"{current_time} - {ctx.author.name} unmuted {member}")

@bot.group(name='lockdown')
@commands.has_permissions(manage_channels = True)
async def lockdown(ctx):
    await ctx.send("Choose lockdown channel or lockdown server. ")


@commands.has_permissions(manage_channels = True)
@lockdown.command(name='channel')
async def lockdownchannel(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
    await ctx.send(f"{current_time} - This channel has been locked down")
    print(f"{current_time} - This channel has been locked down")


@commands.has_permissions(manage_channels = True)
@lockdown.command(name="server")
async def lockdownserver (ctx):
    for channel in ctx.guild.text_channels:
        defrole = ctx.guild.default_role
        perms = channel.overwrites_for(defrole)
        if perms.send_messages == False:
            global channelid
            channelid = {}
            channelid[channel.name] = channel.id
            print(channelid)
        else:
            perms.send_messages = False
            await channel.set_permissions(defrole, overwrite = perms, reason = "Server lockdown")

    await ctx.send("Locked down server")


@commands.has_permissions(manage_channels = True)
@lockdown.command(name="off")
async def lockdownoff(ctx):
    for channel in ctx.guild.text_channels:
        if channel.id in channelid:
            channelid.pop(channel.id)
        else:
            await channel.set_permissions(ctx.guild.default_role, send_messages = True)

    print(channelid)
    await ctx.send("Lockdown removed")
    print(f"{ctx.author.name} has removed the lockdown")

#------MISC COMMANDS-----

@bot.command()
async def ping(ctx):
    ping_ = bot.latency
    ping = round(ping_ * 1000)
    await ctx.send(f"my ping is **{ping} ms**")
    print(f"{current_time} - my ping is {ping} ms")


bot.remove_command("help")

@bot.group(name='help')
async def help(ctx):
    await ctx.send("""Here is the list for the sections in the help command :```
Moderation
Meme
Misc```""")

@help.command(name='moderation')
async def moderation_subcommand(ctx):
    await ctx.send("""Moderation Commands (Commands only allowed to be used by people with the moderator role and up:
    clear (amount): Deletes a set amount of messages, default value is 2
    purge: Deletes all messages in the channel
    ban (user): permanently bans a user from the server
    unban (user): Unbans a user from the server
    kick (user): Kicks a user from the server
    slowmode (time): activates slowmode for a channel, 0 is to turn off, 5 seconds is the default value. (Enter the value without s at the end)""")
@help.command(name='meme')
async def command(ctx):
    await ctx.send('''Meme Commands (Commands that are used for fun):
    walter: Shows an epic picture of walter
    fuck (user): Insults a user that you put in
    fuckzae: FUCK YOU ZAE''')

@help.command(name = 'misc')
async def misc_subcommand(ctx):
    await ctx.send("""Misc Commands:
    afk (time) (status): Sets your AFK status""")

@bot.command()
async def afk(ctx, mins, *,  act : str,):
    current_nick = ctx.author.nick  
    await ctx.send(f"{ctx.author.mention} has gone afk for {mins} minutes. {ctx.author.mention} is {act}")
    await ctx.author.edit(nick=f"{ctx.author.name} [AFK] {act}")

    counter = 0
    while counter <= int(mins):
        counter += 1
        await asyncio.sleep (60)

        if counter == int(mins):
            await ctx.author.edit(nick=current_nick)
            await ctx.send(f"{ctx.author.mention} is no longer AFK")
            break

@bot.command()
@commands.has_permissions(manage_roles = True)
async def rolecolor(ctx, role: str, color: int):
    role = get(ctx.guild.roles, name = role)
    await role.edit(color = discord.Colour(color))

#-----MEME COMMANDS-------

@bot.command()
async def walter(ctx):
    await ctx.send("<:Walter:714316922409320530>")

@bot.command()
async def fuckzae(ctx):
    userid = ctx.guild.get_member(480617726776180741)
    await ctx.send(f"{userid.mention} has a fucking small :eggplant:")

@bot.command()
async def fuck(ctx, member: discord.Member):
    await ctx.send(f"{member.mention} is an absolute retard. :middle_finger: Fuck you ")

@bot.command(pass_context = True, aliases = ["j", "joi"])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await ctx.send(f"Joined {channel}")



@bot.command(pass_context = True, aliases = ["l", "lea"])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"{current_time} - Bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Wow, you really think that I'm in a voice channel do you?")


@bot.command()
async def china(ctx):
    userid = ctx.author.id

    if userid == 349256335742730253:

        voice = get(bot.voice_clients, guild = ctx.guild)

        voice.play(discord.FFmpegPCMAudio("alex.mp3"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        
        
        await ctx.send(f"American Luigi is now Chinese Luigi")

    else:
        await ctx.send("That wasn't very Xie Wua Piao Piao of you. ")


#-----USER INTERACTION COMMANDS-----

@bot.command()
async def marry(ctx, member):
    for x in range(1):
        x = random.randint(1, 101)
        await ctx.send(f"{ctx.author.mention} has a {x}% chance of getting with {member}")
        print(f"{current_time} - {ctx.author.name} asked out {member}")


        if x > 50:
            print(f"{current_time} - {ctx.author.name} has a decent chance at winning over {member}")
            await ctx.send(f"{current_time} - {ctx.author.name} has a decent chance at winning over {member}")
        else:
            print(f"{ctx.author.name} is bouta get rejected lmfao")
            await ctx.send(f"{current_time} - {ctx.author.name} is bouta get rejected lmfao")
        break
#------SERVER COMMANDS-----

@bot.command()
async def membercount(ctx):
    await ctx.send(f":shinto_shrine:**Kenkyona Village** :shinto_shrine: has **{ctx.guild.member_count} members**")
    print(f"{current_time} - {ctx.author.name} used membercount")

#------USER SPECIFIC COMMANDS-----

@bot.command()
async def shutthefuckup(ctx, member: discord.Member):
    userid = ctx.message.author.id 

    if userid == 448649939082412032:
        await ctx.send("Shut the fuck up before I mute ur ass")
        mute_role = get(member.guild.roles, name = 'Muted')
        await member.add_roles(mute_role)
    else:
        await ctx.send("Nice try fuck tard, you can't do that. ")

@bot.command()
async def bruh(ctx, member: discord.Member):
    userid = ctx.message.author.id 

    if userid == 379128692674134016:
        await ctx.send(f"{member.mention} is an absolute clown lol :clown: :clown: :clown:")
    else:
        await ctx.send("Nice try bitch")


'''@bot.command()
async def hello(ctx):'''


bot.loop.create_task(update_stats())
bot.run(token)



#-----UNFINISHED COMMANDS-----

'''
giphy_token = 'p75a4JfMHQIuLlMCYEspoWgjrECIERQb'
api_instance = giphy_client.DefaultApi()

@bot.command()
async def giphy(ctx, *, search):

    embed = discord.Embed(colour=discord.Colour.blue())
    session = aiohttp.ClientSession()

    if search == '':
        response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=p75a4JfMHQIuLlMCYEspoWgjrECIERQb')
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=API_KEY_GOES_HERE&limit=10')
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

    await session.close()

    await ctx.send(embed=embed)'''
