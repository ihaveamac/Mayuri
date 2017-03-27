import discord
from discord.ext import commands
from .util import check, log
from __main__ import messages


class Extras:
    """
    Extra commands that don't fit anywhere else.
    """
    def __init__(self, bot):
        self.bot = bot
        bot.debug("Loaded " + self.__class__.__name__)

    @commands.command()
    async def about(self):
        """Information about this bot"""
        await self.bot.say(
            "I'm Mayuri, the bot by ihaveamac!\n"
            "Find the source for me at"
            "**<https://github.com/ihaveamac/Mayuri>**!"
        )

    @check.fail()
    @commands.command()
    async def failtest(self):
        """Always fail with no permission for testing purposes"""
        await self.bot.say("This message should not happen")

    @commands.command()
    async def errortest(self):
        """Always raise an exception for testing purposes"""
        raise Exception("intended exception")

    @commands.command(pass_context=True)
    async def welcometest(self, ctx):
        """Test welcome text."""
        if messages.WELCOME_MESSAGE:
            await self.bot.say(self.bot.format_message(
                messages.WELCOME_MESSAGE,
                ctx.message.author
            ))
        else:
            await self.bot.say("WELCOME_MESSAGE is empty!")

    @commands.command(pass_context=True)
    async def a(self, ctx):
        await self.bot.say(self.bot.format_message(
            "username={username}\n"
            "username_mention={username_mention}\n"
            "server_name={server_name}\n"
            "welcome_channel={welcome_channel}\n"
            "welcome_channel_mention={welcome_channel_mention}\n"
            "command={command}\n"
            "command_prefixed={command_prefixed}\n"
            "prefix={prefix}\n",
            ctx.message.author,
            ctx=ctx
        ))

    @commands.command(pass_context=True)
    async def b(self, ctx, user, reason):
        await log.log('mod', self.bot.channels['mod-logs'], ctx=ctx,
                      target=ctx.message.mentions[0], action='Action',
                      action_message='Action message', user=ctx.message.author,
                      reason=reason, emoji='FACE WITH TEARS OF JOY')


def setup(bot):
    bot.add_cog(Extras(bot))
