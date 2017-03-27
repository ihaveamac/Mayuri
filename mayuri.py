#!/usr/bin/env python3

__author__ = "Ian (ihaveamac)"
__copyright__ = "Copyright (c) 2017 Ian"
__license__ = "Apache License 2.0"
__version__ = "0.0"

import asyncio
import os
import re
import traceback
from collections import OrderedDict
from sys import argv, exit, stderr

# set working directory to bot folder, in case the script is run in
# a different directory
bot_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(bot_directory)


def debug(msg):
    if core.DEBUG or "--debug" in argv:
        print("DEBUG: " + str(msg))


# import the discord module and print a message if it fails
# this is probably not needed (discord.py requirement should be obvious)
# but could be useful if someone forgot, and it looks cleaner too
try:
    import discord
    from discord.ext import commands
except ImportError:
    exit("Failed to load discord module! Did you forget to install "
         "discord.py?")

# import the config and print a message if it fails
try:
    from config import core, messages, channels, roles, logs
except ImportError:
    exit("Failed to load core config! Did you forget to copy config-example "
         "to config and edit it?")

debug("Debug mode enabled")
debug("Bot directory is " + bot_directory)

if not os.path.isdir("data"):
    debug("Creating data/")
    os.makedirs("data", exist_ok=True)
if not os.path.isfile("data/restrictions.json"):
    debug("Creating data/restrictions.json")
    with open("data/restrictions.json", "w") as f:
        f.write("{}")
if not os.path.isfile("data/staff.json"):
    debug("Creating data/staff.json")
    with open("data/staff.json", "w") as f:
        f.write("{}")
if not os.path.isfile("data/warns.json"):
    debug("Creating data/warns.json")
    with open("data/warns.json", "w") as f:
        f.write("{}")
if not os.path.isfile("data/watches.json"):
    debug("Creating data/watches.json")
    with open("data/watches.json", "w") as f:
        f.write("{}")


bot = commands.Bot(command_prefix=core.COMMAND_PREFIXES,
                   description=core.DESCRIPTION)

bot.debug = debug

# set bot permissions, for when it is invited to servers
# you can also see them here if you want to see what is needed
permissions = discord.Permissions()
permissions.kick_members = True
permissions.ban_members = True
permissions.manage_channels = True
# permissions.add_reactions = True
permissions.read_messages = True
permissions.send_messages = True
permissions.manage_messages = True
permissions.embed_links = True
# permissions.attach_files = True
permissions.read_message_history = True
# permissions.change_nickname = True
# permissions.manage_nicknames = True


# replace multiple strings inside a string - used from:
# http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
def multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(
        lambda match: replace_dict[match.group(0)], string
    )


def multiple_replace(string, *key_values):
    return multiple_replacer(*key_values)(string)


# set a message formatter based on the variables listed in config/messages.py
# this does not take a server as an argument, since it is assumed we're using
# the only server the bot is in, or the one set as SERVER_ID.
def format_message(msg, user, ctx=None):
    formatted_msg = multiple_replace(msg, *(
        ('{username}', user.name),
        ('{username_mention}', user.mention),
        ('{server_name}', bot.main_server.name)
    ))
    if ctx and ctx.invoked_with:
        formatted_msg = multiple_replace(formatted_msg, *(
            ('{command}', ctx.invoked_with),
            ('{command_prefixed}', ctx.prefix + ctx.invoked_with),
            ('{prefix}', ctx.prefix)
        ))
    if bot.channels['welcome']:
        formatted_msg = multiple_replace(formatted_msg, *(
            ('{welcome_channel}', bot.channels['welcome'].name),
            ('{welcome_channel_mention}', bot.channels['welcome'].mention)
        ))
    else:
        formatted_msg = multiple_replace(formatted_msg, *(
            ('{welcome_channel}',
             "(set WELCOME_CHANNEL in config/channels.py!)"),
            ('{welcome_channel_mention}',
             "(set WELCOME_CHANNEL in config/channels.py!)")
        ))
    return formatted_msg


bot.format_message = format_message

# set the bot's server id early
# if it stays '' in the config then it is set to the server the bot is in
bot.server_id = core.SERVER_ID

# create all_ready, to indicate the bot is fully ready
# this is set after on_ready has finished, so commands/events can be used
# TODO: this
bot.all_ready = False
bot._is_all_ready = asyncio.Event(loop=bot.loop)


async def wait_until_all_ready():
    """Wait until the entire bot is ready."""
    await bot._is_all_ready.wait()

bot.wait_until_all_ready = wait_until_all_ready


# check the bot's servers, which usually should only contain one
# set channel and role variables based on config options
@bot.event
async def on_ready():
    if bot.all_ready:
        return
    debug("Bot is in {0} servers".format(len(bot.servers)))
    if len(bot.servers) == 0:
        await bot.close()
        print(
            "This bot is not in any servers! Use this to put me in one!\n  "
            + discord.utils.oauth_url(bot.user.id, permissions=permissions)
        )
        return
    if len(bot.servers) > 1:
        # TODO: handle SERVER_ID
        if core.SERVER_ID != '':
            bot.main_server = discord.utils.get(bot.servers, id=core.SERVER_ID)
        else:
            await bot.close()
            print(
                "This bot account should only be in one server. If you want "
                "to keep it in more than one server, set SERVER_ID in "
                "config/core.py to the ID of the server you want the bot to "
                "operate in."
            )
            return
    else:
        # get the only server in the list and set it as the main server
        bot.main_server = list(bot.servers)[0]
        if core.SERVER_ID != '':
            bot.server_id = core.SERVER_ID
            if bot.main_server.id != bot.server_id:
                # this needs to be made more readable
                await bot.close()
                print(
                    "Server ID mismatch! SERVER_ID is " + core.SERVER_ID + ", "
                    "but bot is only in " + bot.main_server.id + "\n"
                    "To invite it to this server, use this invite link:\n  "
                    + discord.utils.oauth_url(bot.user.id,
                                              permissions=permissions)
                    + "\nor change SERVER_ID in config/core.py"
                )
                return
        else:
            bot.server_id = bot.main_server.id

    debug("Setting channels")
    bot.channels = {}
    # kind of a crappy workaround to close the bot if setting something fails
    setting_successful = True

    # quickly set multiple keys for channels and roles
    def set_key(key, name, dict, iterable, extra=None):
        if name[0] == '#' or name[0] == '&':
            object = discord.utils.get(
                iterable,
                name=name[1:]
            )
        else:
            object = discord.utils.get(
                iterable,
                id=name
            )
        if object:
            if key:
                # only used for static roles (staff, muted, etc)
                dict[key] = object
                debug("Set key " + key + " to object ID " + dict[key].id)
            else:
                # only used for dynamic roles (staff ranks)
                # which will have an extra value
                dict[object.name] = (object, extra)
                debug("Set key " + object.name + " to object ID "
                      + dict[object.name][0].id)
        else:
            setting_successful = False
            print(
                "Failed to set channel with key \"" + key + "\"\n"
                "Tried to use name/id " + name
            )
            return

    # welcome channel is the only one that can fail
    # because some servers may not have or want it
    if channels.WELCOME_CHANNEL:
        set_key('welcome', channels.WELCOME_CHANNEL, bot.channels,
                bot.main_server.channels)
    else:
        bot.channels['welcome'] = None
    set_key('mods', channels.MODS_CHANNEL, bot.channels,
            bot.main_server.channels)
    set_key('mod-logs', channels.MOD_LOGS_CHANNEL, bot.channels,
            bot.main_server.channels)
    set_key('server-logs', channels.SERVER_LOGS_CHANNEL, bot.channels,
            bot.main_server.channels)
    set_key('message-logs', channels.MESSAGE_LOGS_CHANNEL, bot.channels,
            bot.main_server.channels)
    if not setting_successful:
        await self.bot.close()
        return

    debug("Setting roles (non-staff ranks)")
    bot.roles = {}
    set_key('staff', roles.MAIN_STAFF_ROLE, bot.roles, bot.main_server.roles)
    set_key('muted', roles.MUTED_ROLE, bot.roles, bot.main_server.roles)
    set_key('no-embed', roles.NO_EMBED_ROLE, bot.roles, bot.main_server.roles)
    if not setting_successful:
        await self.bot.close()
        return

    debug("Setting roles (staff ranks)")
    bot.staff_roles = OrderedDict()
    for staff_rank in roles.STAFF_ROLES:
        set_key(None, staff_rank[0], bot.staff_roles, bot.main_server.roles,
                extra=staff_rank[1])
    if not setting_successful:
        await self.bot.close()
        return

    bot.all_ready = True
    bot._is_all_ready.set()
    print("{0.user} is all up and running!".format(bot))


# only process messages from the server we're in
@bot.event
async def on_message(message):
    if message.server.id != bot.server_id:
        return

    await bot.process_commands(message)


# handle errors and print a message if a command fails
# some code taken from
# https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/bot.py
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.errors.CommandNotFound):
        if messages.NONEXISTANT_COMMAND_MESSAGE != "":
            msg = format_message(
                messages.NONEXISTANT_COMMAND_MESSAGE,
                ctx.message.author, ctx=ctx
            )
            await bot.send_message(ctx.message.channel, msg)
    elif isinstance(error, commands.errors.CheckFailure):
        if messages.NO_PERMISSION_MESSAGE != "":
            msg = format_message(
                messages.NO_PERMISSION_MESSAGE,
                ctx.message.author, ctx=ctx
            )
            await bot.send_message(ctx.message.channel, msg)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        if messages.MISSING_ARGUMENTS_MESSAGE != "":
            formatter = commands.formatter.HelpFormatter()
            # formatter.format_help_for(ctx, ctx.command)[0]
            msg = format_message(
                messages.MISSING_ARGUMENTS_MESSAGE,
                ctx.message.author, ctx=ctx
            )
            if messages.MISSING_ARGUMENTS_APPEND_HELP:
                msg += formatter.format_help_for(ctx, ctx.command)[0]
            await bot.send_message(ctx.message.channel, msg)
    else:
        print('Ignoring exception in command {0.command}'.format(ctx),
              file=stderr)
        traceback.print_exception(type(error), error, error.__traceback__,
                                  file=stderr)
        if ctx.invoked_with:
            if messages.COMMAND_ERROR_MESSAGE != "":
                msg = format_message(
                    messages.COMMAND_ERROR_MESSAGE,
                    ctx.message.author, ctx=ctx
                )
                await bot.send_message(ctx.message.channel, msg)


# load all of the listed default cogs before running the bot
debug("Loading cogs")
cogs = ("extras", "cleanup", "memberevents", "restrictions")
for cog in cogs:
    debug("Loading cogs." + cog)
    bot.load_extension("cogs." + cog)

# run the bot!
debug("Running bot")
print("Mayuri " + __version__ + "!")
bot.run(core.TOKEN)
