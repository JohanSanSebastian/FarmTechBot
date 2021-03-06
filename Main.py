import discord
import asyncio
import time
import random
import re
import aiohttp
from datetime import datetime
from discord.ext import commands
from pyrandmeme import *

intents = discord.Intents().all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command("help")
token = "Your_Bot_Token"


@client.event
async def on_member_join(member):
    wlcmChannel = client.get_channel(Your_welcome_channel)
    await wlcmChannel.send(f'Welcome {member.mention}........To the official FarmTech Server')

    role = member.guild.get_role(your_member_role)
    await member.add_roles(role)


@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')
    await client.change_presence(activity=discord.Game('Helping FarmTech Members'))

######################################### Kick Command #######################################
@client.command()
@commands.has_any_role("Admin")
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
    if reason == None:
        await user.kick(reason=reason)
        await ctx.send(f"{user} have been kicked sucessfully")
    else:
        await user.kick(reason=reason)
        await ctx.send(f"{user} have been kicked sucessfully because {reason}")

################################### Ban Command ########################################
@client.command()
@commands.has_any_role("Mod")
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    if reason == None:
        await user.ban(reason=reason)
        await ctx.send(f"{user} have been bannned sucessfully")
    else:
        await user.ban(reason=reason)
        await ctx.send(f"{user} have been bannned sucessfully because of {reason}")

    mod_channel = client.get_channel(mod_log_channel)

    ban_embed = discord.Embed(title="Ban", color=0xe44225)
    ban_embed.add_field(
        name=f"{user} was banned by", value=ctx.message.author, inline=False)
    ban_embed.set_footer(
        text=f"{ctx.guild.name}  •  {datetime.strftime(datetime.now(), '%d.%m.%Y at %I:%M %p')}")

    await mod_channel.send(embed=ban_embed)

######################################## Unban Command ########################################
@client.command(pass_context=True)
@commands.has_any_role("Admin")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user):
    member = str(user)
    member = member.replace("<", "")
    member = member.replace(">", "")
    member = member.replace("@", "")
    member = member.replace("!", "")
    member_unban = discord.Object(id=member)
    # user = client.get_user_info(member)
    await ctx.guild.unban(member_unban)
    await ctx.send(f"Unbanned {user}")

    member_mention = await client.fetch_user(member)
    mod_channel = client.get_channel(mod_log_channel)

    unban_embed = discord.Embed(title="Unban", color=0xe44225)
    unban_embed.add_field(
        name=f"{member_mention} was unbanned by", value=ctx.message.author, inline=False)
    unban_embed.set_footer(
        text=f"{ctx.guild.name}  •  {datetime.strftime(datetime.now(), '%d.%m.%Y at %I:%M %p')}")

###################################### Unban using ID Command #####################################
@client.command(pass_context=True)
@commands.has_any_role("Admin")
@commands.has_permissions(ban_members=True)
async def unbanMember(ctx, *, member):
    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.send(f"Unbanned {user.mention}")

    mod_channel = client.get_channel(mod_log_channel)

    unban_embed = discord.Embed(title="Unban", color=0xe44225)
    unban_embed.add_field(
        name=f"{member} was unbanned by", value=ctx.message.author, inline=False)
    unban_embed.set_footer(
        text=f"{ctx.guild.name}  •  {datetime.strftime(datetime.now(), '%d.%m.%Y at %I:%M %p')}")
    await mod_channel.send(embed=unban_embed)

################################### Poll Command #######################################
@client.command(pass_context=True, add_reactions=True)
async def poll(ctx, *, message):

    polls = discord.Embed(title="Idea", color=0x31d2dd)
    polls.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/810546790172590166/814071210233167892/Green_School_Science_Club_Logo_2.png")
    polls.add_field(name=message, value=ctx.message.author, inline=False)
    polls.set_footer(
        text=f"{ctx.guild.name}  •  {datetime.strftime(datetime.now(), '%d.%m.%Y at %I:%M %p')}")

    pollsChannel = client.get_channel(poll_channel)

    reactmsg = await pollsChannel.send(embed=polls)
    await reactmsg.add_reaction("👍")
    await reactmsg.add_reaction("👎")

###################################### Clear Command ###################################
@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount+1)

###################################### Nuke Command ####################################
@client.command()
@commands.has_any_role("Head")
@commands.has_permissions(ban_members=True)
async def nuke(ctx):
    embed = discord.Embed(
        color=0x2555e4,
        title=f":boom: Channel ({ctx.channel.name}) has been nuked :boom:",
        description=f"Nuked by: {ctx.author.name}#{ctx.author.discriminator}"
    )
    embed.set_footer(
        text=f"{ctx.guild.name}  •  {datetime.strftime(datetime.now(), '%d.%m.%Y at %I:%M %p')}")
    await ctx.channel.delete(reason="nuke")
    channel = await ctx.channel.clone(reason="nuke")
    await channel.send(embed=embed)

###################################### Ping Command #####################################
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! Its `{round(client.latency * 1000)}ms`')

###################################### Echo Command ######################################
@client.command()
async def echo(ctx, *, arg):
    await ctx.send(arg)

####################################### Embed Command ####################################
@client.command()
async def embed(ctx, channel, title, *, message):

    embed = discord.Embed(title=title, description=message, color=0xe1ff00)
    channel = client.get_channel(int(channel))

    await channel.send(embed=embed)

######################################## Eval Command ####################################
@client.command(name='eval')
@commands.is_owner()
async def _eval(ctx, *, cmd):
    await ctx.send(f"```{eval(cmd)}```")

######################################### Meme Command ####################################
@client.command(pass_context=True) 
async def meme(ctx):
    embed = discord.Embed(title="Meme", description=None)

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/wholesomememes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed, content=None)
    
######################################## Help Command #####################################
@client.command()
async def help(ctx):
    help_embed = discord.Embed(title="All the commands of FarmTechBot", url="https://www.farmtech.gq",
                               description="To get this message use `!help`", color=0x25e432)
    help_embed.set_author(name="Help")
    help_embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/810546790172590166/814071210233167892/Green_School_Science_Club_Logo_2.png")
    help_embed.add_field(name="1. User Commands",
                         value="Commands all users can use", inline=False)
    help_embed.add_field(
        name="`!poll`", value="To add a poll with your idea", inline=True)
    help_embed.add_field(
        name="`!echo`", value="To echo any message", inline=True)
    help_embed.add_field(
        name="`!ping`", value="To find out ping", inline=True)
    help_embed.add_field(
        name="`!meme`", value="You know what this does", inline=True)
    
    help_embed.add_field(name="2. Mod Commands",
                         value="Commands only Mod/Admin/Head can use", inline=False)
    help_embed.add_field(name="`!ban`", value="To ban a user", inline=True)
    help_embed.add_field(name="`!clear`", value="To delete mulitple messages", inline=True)
    help_embed.add_field(name="3. Admin Commands",
                         value="Commands only Admin/Head can use", inline=False)
    help_embed.add_field(
        name="`!kick`", value="To directly kick a member", inline=True)
    help_embed.add_field(
        name="`!unban`", value="To unban a member", inline=True)
    
    help_embed.add_field(name="3. Head Commands",
                         value="Commands only Heads can use", inline=False)
    help_embed.add_field(
        name="`!nuke`", value="To nuke a channel", inline=True)
    help_embed.add_field(
        name="`!embed`", value="To send an embed", inline=True)
    
    help_embed.set_footer(
        text=f"{ctx.guild.name}  •  {datetime.strftime(datetime.now(), '%d.%m.%Y at %I:%M %p')}")
    await ctx.send(embed=help_embed)

######################################### Client Run ########################################
client.run(token)
