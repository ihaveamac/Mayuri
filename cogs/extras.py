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


def setup(bot):
    bot.add_cog(Extras(bot))
