import discord
from discord import Server
from discord import Client
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

bot = commands.Bot(command_prefix='$')
key = open('testkey.txt').readline().rstrip('\n')
messages = ["$$a flcl","$$a ","$$a mha","https://osu.ppy.sh/beatmapsets/717528#osu/1515830","https://osu.ppy.sh/beatmapsets/591442","https://osu.ppy.sh/beatmapsets/1#osu/1","$$v remo con || wan opo","$$v a || yunosuke","$$v s || lazy","$$v a || sdnjsb", "$$v s || gjdgjksd","$$v s || catlife","$$v undead enemy","$$v a || ","$$v s || "]
loopvalue = 0

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')
    #
    #tests begin here
    #
    global chan
    chan = bot.get_channel('431806042377289739')

@bot.event
async def on_message(message):
    global loopvalue
    if message.author.id != bot.user.id:
        if message.content == "reset":loopvalue=0
        else:
            await bot.send_message(chan, messages[loopvalue])
            loopvalue += 1
    await bot.process_commands(message)



bot.run(key)
