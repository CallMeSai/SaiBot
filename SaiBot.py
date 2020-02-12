import asyncio
import discord
from discord import Guild as Server
from discord.ext import commands
from discord.ext.commands import Bot
import requests
import sys
import json
import datetime
from pathlib import Path
from anime import anime
from osu import osu
import re
from voca import voca
import subprocess
import youtube_dl
from rewrite import Music

#read key from file
key = json.load(open('saikey.txt'))

osuapi = "https://osu.ppy.sh/api/get_beatmaps?k=" + str(key['osu'])
vocaapi = "https://vocadb.net/api"
#xivdb = "https://api.xivdb.com/"

#osu gamemodes
modes = ['osu','taiko','fruits','mania']

#declare command prefix
bot = commands.Bot(command_prefix='$$')

#remove default help command
bot.remove_command('help')

#when bot initialised, change game and print bot details to screen
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name='with catnip'))
    global me
    me = bot.get_user(155421790963892224)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')

#
# --COMMANDS--
#If message starts with command prefix, read command word and reply
#

@bot.command(pass_context = True)
async def clear(ctx):
    channel = ctx.channel
    if ctx.message.author == me: await ctx.purge()
    else: await channel.send("You are not permitted to do that")

#Help command helps users understand how to use SaiBot
@bot.command(pass_context = True)
async def help(ctx):
    channel = ctx.channel
    await channel.send("```Commands:\n\t$$a <anime name> - Get information on anime\n\t$$boost - boost\n\t$$BOOST - BOOST\n\t$$help - How did you get here?\n\t$$v <song> || <artist> - Get info on vocaloid songs\n\n\tYou can also search for only a song with $$v s || <songname> and only an artist with $$v a || <artistname>\n\n\tosu! links - Paste an osu beatmap and get info on the map/s ```\nSend Sai a DM if anything breaks or if you have a good idea for a new feature.\nYou can also DM me commands if you don't want people to see your weeb stuff.")

@bot.command(pass_context = True)
async def boost(ctx):
    channel = ctx.channel
    await channel.send("https://b.catgirlsare.sexy/QwAa.jpg")

@bot.command(pass_context = True)
async def BOOST(ctx):
    channel = ctx.channel
    await channel.send("https://i.imgur.com/Yvf3htW.gif")
#--ANIME COMMAND--
#Split message by new line, pop first element in list, split again by spaces.
#Delete command from message and join elements with a space between each.
#Call anime function and send embed message.

@bot.command(pass_context = True)
async def a(ctx):
    channel = ctx.channel
    split_message = ctx.message.content.split('\n').pop(0).split(' ')
    del split_message[0]
    split_message = ' '.join(split_message)
    if split_message == '': await channel.send("<@" + ctx.message.author.id + ">, please enter an anime name")
    #if fail DM error to dev
    else:
        try:
            embed = anime(split_message)
            if str(embed) == "NoValue": await channel.send("Sorry, <@" + ctx.message.author.id + ">, I couldn't find anything. Please check your spelling or check $$help.")
            else: await channel.send(embed=embed)
        except Exception as err:
            await channel.send("Sorry, something broke. A message has been sent to Sai to fix this")
            await me.send("Uuwahh! Senpai! Something broke!\n ``` " + str(err) + " ```")
#--VOCALOID COMMAND--
#Change text to lowercase, remove command characters, split by || characters
#Call voca function and send embed message
@bot.command(pass_context = True)
async def v(ctx):
    try:
        channel = ctx.channel
        vocamsg = ctx.message.content.lower().lstrip('$$v ').split(' || ')
        if vocamsg[0] == '' or vocamsg[0] == '':
            await channel.send("Sorry, <@" + ctx.message.author.id + ">, you cannot enter a blank argument")
        else:
            embed = voca(vocamsg)
            #if fail reply typical errors
            if str(embed) == "IndexError":
                await channel.send("Sorry, <@" + ctx.message.author.id + ">, I didn't catch that. Make sure the request format is <song> || <artist> or <s/a> || <song/artist>.")
            if str(embed) == "NoValue":
                await channel.send("Sorry, <@" + ctx.message.author.id + ">, I couldn't find anything. Please check your spelling or check $$help.")
            else:
                await channel.send(embed = embed)
    #if error isn't a typical error, send fail response and DM error to dev
    except Exception as err:
        await channel.send('Sorry, something broke. A message has been sent to Sai to fix this')
        await me.send("Uuwahh! Senpai! Something broke!\n ``` " + str(err) + " ```")

#
# --COMMANDS END--
#
# --OSU FUNCTION--
#check message isn't sent by bot. if the message contains osu beatmap url check
#  if the url contains one of the 4 gamemodes and split at the modeself
#call osu function and send embed message
@bot.event
async def on_message(message):
    channel = message.channel
    if message.author.id != bot.user.id:
        if 'osu.ppy.sh/beatmapsets/' in message.content:
            osumsg = [e for e in re.split('[/#]',message.content.split('beatmapsets/').pop()) if e not in modes]
            if osumsg[0] == '' or int(osumsg[0]) < 1: await me.send(message.channel,'Sorry,<@' + message.author.id + '>, you cannot enter nothing or a value less than 1')
            else:
                try:
                    embed = osu(osumsg,key['osu'])
                    if str(embed) == "NoValue":
                        await channel.send(message.channel,'Sorry, <@' + message.author.id + ">, I couldn't find that beatmap. Please check your ID is correct.")
                    else: await channel.send(message.channel,embed=embed)
                #if fail send fail response and DM error to dev
                except Exception as err:
                    await me.send("Uuwahh! Senpai! Something broke!\n ``` " + str(err) + " ```")
                    await channel.send(message.channel,'Sorry, something broke. A message has been sent to Sai to fix this')

    await bot.process_commands(message)

bot.add_cog(Music(bot))
bot.run(str(key["discord"]))