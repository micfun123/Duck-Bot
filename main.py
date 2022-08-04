from http import client
from itertools import chain
import discord
from discord.ext import commands
import asyncio
import json
import random
import os
from os import listdir
from os.path import isfile, join

import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv

load_dotenv()


client = commands.Bot(command_prefix="^", case_insensitive=True, intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot is ready!")
    await client.change_presence(activity=discord.Game(name="quack"))

@client.event
async def on_guild_join(guild):
    filename = "servers.json"
    with open(filename, "r") as f:
        data = json.load(f)
    append = {
        "guild_id": guild.id,
        "channel": None
    }
    data.append(append)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
       
@client.event
async def on_guild_remove(guild):
    filename = "servers.json"
    with open(filename, "r") as f:
        data = json.load(f)
    for i in range(len(data)):
        if data[i]["guild_id"] == guild.id:
            data.pop(i)
            break
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

@client.command()
async def setchannel(ctx, channel: discord.TextChannel):
    filename = "servers.json"
    with open(filename, "r") as f:
        data = json.load(f)
    for i in range(len(data)):
        if data[i]["guild_id"] == ctx.guild.id:
            data[i]["channel"] = channel.id
            break
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
        await ctx.send(f"Set channel to {channel.mention}")
        return



@client.event
async def on_message(message):
    filename = "servers.json"
    with open(filename, "r") as f:
        data = json.load(f)
    for i in range(len(data)):
        if message.channel.id == data[i]["channel"]:
            if message.author.bot:
                    return
            else:
                    
                    messageamount = random.randint(1, 5)
                    duck = "quack " * messageamount
                    await message.channel.send(duck)
        else:
            await client.process_commands(message)



token = os.getenv("DISCORD_TOKEN")

client.run(token)
