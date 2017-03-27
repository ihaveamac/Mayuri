import discord
from discord.ext import commands
from .util import check, msg_util, restrict, log


class Restrictions:
    """
    User restrictions such as mute and no-embed.
    """
    def __init__(self, bot):
        self.bot = bot
        bot.debug("Loaded " + self.__class__.__name__)

    @check.is_staff()
    @commands.command(pass_context=True, description="Mute user",
                      brief="Mute a user")
    async def mute(self, ctx, user, reason=''):
        """
        Mute a user, removing their ability to send messages to channels.

        This notifies the targeted user, including the reason if one is
        provided.

        This applies the role set in the config. This role should be configured
        for every channel where users can speak. For easy setup, see the
        `rolesetup` command.

        This restriction persists when the user leaves and re-joins, until it
        is removed with the `unmute` command.
        """
        target = msg_util.get_user_from_mention(ctx.message.mentions, user)
        if not target:
            if user[0:2] == '<@':
                await self.bot.say("This member is not in the server.")
            elif user[0] == '@':
                await self.bot.say("A member was not properly mentioned. Make"
                                   "sure the target is in this server.")
            else:
                await self.bot.say("No member was mentioned.")
            return
        restrict.add_restriction(target.id, 'mute')
        try:
            await self.bot.send_message(
                target,
                "You were muted from {0.name}!"
                "The given reason is: {1}".format(self.bot.server, reason)
            )
        await self.bot.say("{0.mention} has been muted.".format(target))
        await log.log('mod', self.bot.channels['mod-logs'], ctx=ctx,
                      target=target, action='Muted', action_message='muted',
                      user=ctx.message.author, reason=reason,
                      emoji='SPEAKER WITH CANCELLATION STROKE')


def setup(bot):
    bot.add_cog(Restrictions(bot))
