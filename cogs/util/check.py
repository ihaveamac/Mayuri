import discord
from discord.ext import commands

# some of this is from Luc#5653's help, who got it from RoboDanny


def permission_check():
    """test"""

    def predicate(ctx):
        message = ctx.message
        if core.SERVER_ID != "" and ctx.message.server.id != core.SERVER_ID:
            return False
        author = message.author
        return True

    return commands.check(predicate)


def is_staff():
    """Check if the user is staff."""
    return commands.check(lambda ctx: ctx.bot.roles['staff']
                          in ctx.message.author.roles)


def fail():
    """Always return "no permission". Used for testing."""

    def predicate(ctx):
        return False

    return commands.check(predicate)
