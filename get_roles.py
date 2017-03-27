#!/usr/bin/env python3

from sys import argv, exit

try:
    import discord
except ImportError:
    exit("Failed to load discord module! Did you forget to install "
         "discord.py?")

try:
    from config import core
except ImportError:
    exit("Failed to load core config! Did you forget to copy config-example "
         "to config and edit it?")

client = discord.Client()


@client.event
async def on_ready():
    for server in client.servers:
        print("{} - {}".format(server.name, server.id))
        for role in server.roles:
            print("  {:32} - {}".format(role.name, role.id))
    await client.close()

try:
    client.run(core.TOKEN)
except discord.errors.LoginFailure:
    exit("Failed to login! Did you set the proper token in core.py? Only bot "
         "tokens are accepted.")
