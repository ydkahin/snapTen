#Created by ydkahin | github.com/ydkahin
import discord
from discord.ext import commands
import random
import asyncio
import datetime

description = '''A simple discord bot that turns text channels to
SnapChat like channels with a limit of 10 messages, after which the 
channel clears everything. 
The limit of 10 messags can easily be adjusted.'''

command_prefix=',' #This can be anything as long as it doesn't conflict with other bots' prefixes
bot = commands.Bot(command_prefix, description)
perm = discord.Permissions
mes = discord.Message
client = discord.Client

channels_to_delete_from = [] #We will store the names of the channels that will run this bot

@bot.command(pass_context = True)
async def only10(ctx, chan : discord.TextChannel = None):
    member = ctx.message.author
    if chan is None:
        chan = ctx.channel #If a channel is not 
    if member.guild_permissions >= perm.text():
        channels_to_delete_from.append(chan.name)
        await ctx.send("SnapTen is now running on #" + chan.name + ".")
    else:
        await ctx.send("You don't have enough permissions on this channel to perform this!")



@bot.command(pass_context = True)
async def notonly10(ctx, chan : discord.TextChannel = None):
    member = ctx.message.author
    if chan is None:
        chan = ctx.channel #If a channel is not 
    if member.guild_permissions >= perm.text(): #The user running this command must have the permission to manage messages in the specified channel
        try: 
            channels_to_delete_from.remove(chan.name)
            await ctx.send("SnapTen is no longer running on #" + chan.name + ".")
        except ValueError:
            await ctx.send("SnapTen was not running on this channel!")
    else:
        await ctx.send("You don't have enough permissions on this channel to perform this!")

bot.counter = 0

#The Number Unicode Emojis. The code below can be easily automated, but for the time being, what's here is fine for 10 messages.
num_emoji = [u"\u0030\u20E3", u"\u0031\u20E3", u"\u0032\u20E3", u"\u0033\u20E3", u"\u0034\u20E3", u"\u0035\u20E3", u"\u0036\u20E3", u"\u0037\u20E3", u"\u0038\u20E3", u"\u0039\u20E3"]

@bot.event
async def on_message(message):
    if str(message.channel) in channels_to_delete_from:
        bot.counter += 1
        if bot.counter <=9:
            await message.add_reaction(num_emoji[bot.counter])
        if bot.counter == 9:
            await message.channel.send("Just one left!")
        if bot.counter > 10:
            await message.channel.purge()
            bot.counter = 0
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run('') #Insert your bot token here