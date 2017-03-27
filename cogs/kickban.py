import discord
from discord.ext import commands


class KickBan:
    """
    Commands for kicking and banning users.
    """
    def __init__(self, bot):
        self.bot = bot
        bot.debug("Loaded " + self.__class__.__name__)


def setup(bot):
    bot.add_cog(KickBan(bot))
