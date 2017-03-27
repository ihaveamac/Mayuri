import discord
from discord.ext import commands
from .util import check, log


class Cleanup:
    """
    Cleaning up messages.
    """
    def __init__(self, bot):
        self.bot = bot
        bot.debug("Loaded " + self.__class__.__name__)

    @check.is_staff()
    @commands.command(pass_context=True, description="Clear messages",
                      brief="Delete messages from a channel")
    async def clear(self, ctx, count: int, channel='current'):
        """
        Delete specified messages from a channel. If a channel is not
        specified, the current channel will be used.
        """
        clear_from = ctx.message.channel
        if channel != 'current':
            clear_from = ctx.message.channel_mentions[0]
        await self.bot.purge_from(clear_from, limit=count)
        await log.log('mod', self.bot.channels['mod-logs'], action="Clean up",
                      user=ctx.message.author, target=clear_from,
                      action_message="cleared {} messages from".format(count),
                      emoji='WASTEBASKET')


def setup(bot):
    bot.add_cog(Cleanup(bot))
