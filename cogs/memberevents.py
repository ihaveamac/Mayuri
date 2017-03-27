import discord
from discord.ext import commands
from .util import log
from __main__ import messages


class MemberEvents:
    """
    Events relating to members, including join, leave, and ban logs.
    """
    def __init__(self, bot):
        self.bot = bot
        bot.debug("Loaded " + self.__class__.__name__)

    async def on_member_join(self, member):
        # TODO: welcome message stuff
        await log.log('join', self.bot.channels['server-logs'], target=member)
        if messages.WELCOME_MESSAGE:
            await self.bot.send_message(
                member, self.bot.format_message(messages.WELCOME_MESSAGE,
                                                member)
            )

    async def on_member_remove(self, member):
        await log.log('leave', self.bot.channels['server-logs'], target=member)


def setup(bot):
    bot.add_cog(MemberEvents(bot))
