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
    async def mute(self, ctx, user, *, reason=''):
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
        target = await msg_util.get_user_from_mention(ctx.message.mentions,
                                                      user)
        try:
            await restrict.add_restriction_to_user(target, 'muted')
        except discord.errors.Forbidden:
            await self.bot.say("Failed to add the restriction. Make sure the "
                               "bot has \"Manage Roles\" and the bot's role "
                               "is above the role you want to apply.")
            return
        msg = "You were muted from {0.name}! ".format(self.bot.main_server)
        if reason != "":
            msg += "The given reason is: {0}".format(reason)
        await self.bot.send_message(target, msg)
        await self.bot.say("{0.mention} has been muted.".format(target))
        await log.log('mod', self.bot.channels['mod-logs'], ctx=ctx,
                      target=target, action='Muted', action_message='muted',
                      user=ctx.message.author, reason=reason,
                      emoji='SPEAKER WITH CANCELLATION STROKE')

    @check.is_staff()
    @commands.command(pass_context=True, description="Unmute user",
                      brief="Unmute a user")
    async def unmute(self, ctx, user, *, reason=''):
        """
        Unmute a user, restoring their ability to send messages to channels.

        This removes the role set in the config. This role should be configured
        for every channel where users can speak. For easy setup, see the
        `rolesetup` command.
        """
        target = await msg_util.get_user_from_mention(ctx.message.mentions,
                                                      user)
        try:
            await restrict.remove_restriction_from_user(target, 'muted')
        except discord.errors.Forbidden:
            await self.bot.say("Failed to remove the restriction. Make sure "
                               "the bot has \"Manage Roles\" and the bot's "
                               "role is above the role you want to apply.")
            return
        await self.bot.say("{0.mention} has been unmuted.".format(target))
        await log.log('mod', self.bot.channels['mod-logs'], ctx=ctx,
                      target=target, action='Unmuted',
                      action_message='unmuted', user=ctx.message.author,
                      reason=reason, emoji='SPEAKER')

    @check.is_staff()
    @commands.command(pass_context=True,
                      description="Remove upload permissions",
                      brief="Remove a user's upload permissions",
                      aliases=('noupload',))
    async def rmupload(self, ctx, user, *, reason=''):
        """
        Remove a user's ability to upload files. This does not remove link
        previews, use `rmpreview` to remove this or `rmembed` to remove both
        upload and link previews with one command.

        This notifies the targeted user, including the reason if one is
        provided.

        This applies the role set in the config. This role should be configured
        for every channel where users can upload files. For easy setup, see the
        `rolesetup` command.

        This restriction persists when the user leaves and re-joins, until it
        is removed with the `resupload` or `resembed` commands.
        """
        target = await msg_util.get_user_from_mention(ctx.message.mentions,
                                                      user)
        try:
            await restrict.add_restriction_to_user(target, 'no-upload')
        except discord.errors.Forbidden:
            await self.bot.say("Failed to add the restriction. Make sure the "
                               "bot has \"Manage Roles\" and the bot's role "
                               "is above the role you want to apply.")
            return
        msg = "You lost file upload permissions from {0.name}! ".format(
            self.bot.main_server
        )
        if reason != "":
            msg += "The given reason is: {0}".format(reason)
        await self.bot.send_message(target, msg)
        await self.bot.say("{0.mention} has lost upload permissions.".format(
            target
        ))
        await log.log('mod', self.bot.channels['mod-logs'], ctx=ctx,
                      target=target, action='Remove Upload',
                      action_message='removed upload permissions from',
                      user=ctx.message.author, reason=reason,
                      emoji='CROSS MARK')

    @check.is_staff()
    @commands.command(pass_context=True,
                      description="Restore upload permissions",
                      brief="Restore a user's upload permissions",)
    async def resupload(self, ctx, user, *, reason=''):
        """
        Restore a user's ability to upload files.

        This removes the role set in the config. This role should be configured
        for every channel where users can upload files. For easy setup, see the
        `rolesetup` command.
        """
        target = await msg_util.get_user_from_mention(ctx.message.mentions,
                                                      user)
        try:
            await restrict.remove_restriction_from_user(target, 'no-upload')
        except discord.errors.Forbidden:
            await self.bot.say("Failed to remove the restriction. Make sure "
                               "the bot has \"Manage Roles\" and the bot's "
                               "role is above the role you want to remove.")
            return
        await self.bot.say("{0.mention} has upload permissions"
                           "restored.".format(target))
        await log.log('mod', self.bot.channels['mod-logs'], ctx=ctx,
                      target=target, action='Restore Upload',
                      action_message='restored upload permissions to',
                      user=ctx.message.author, reason=reason,
                      emoji='HEAVY LARGE CIRCLE')

    @check.is_staff()
    @commands.command(pass_context=True,
                      description="Remove link previews",
                      brief="Remove link previews from a user",
                      aliases=('nopreview',))
    async def rmpreview(self, ctx, user, *, reason=''):
        """
        Remove link previews from a user. This does not remove upload
        permissions, use `rmupload` to remove this or `rmembed` to remove both
        upload and link previews with one command.

        This notifies the targeted user, including the reason if one is
        provided.

        This applies the role set in the config. This role should be configured
        for every channel where users have link previews. For easy setup, see
        the `rolesetup` command.

        This restriction persists when the user leaves and re-joins, until it
        is removed with the `respreview` or `resembed` commands.
        """
        target = await msg_util.get_user_from_mention(ctx.message.mentions,
                                                      user)
        try:
            await restrict.add_restriction_to_user(target, 'no-preview')
        except discord.errors.Forbidden:
            await self.bot.say("Failed to add the restriction. Make sure the "
                               "bot has \"Manage Roles\" and the bot's role "
                               "is above the role you want to apply.")
            return
        msg = "You lost link previews from {0.name}! ".format(
            self.bot.main_server
        )
        if reason != "":
            msg += "The given reason is: {0}".format(reason)
        await self.bot.send_message(target, msg)
        await self.bot.say("{0.mention} has lost link previews.".format(
            target
        ))
        await log.log('mod', self.bot.channels['mod-logs'], ctx=ctx,
                      target=target, action='Remove Link Previews',
                      action_message='removed link previews from',
                      user=ctx.message.author, reason=reason,
                      emoji='CROSS MARK')

    @check.is_staff()
    @commands.command(pass_context=True,
                      description="Restore link previews",
                      brief="Restore link previews to a user")
    async def respreview(self, ctx, user, *, reason=''):
        """
        Restore link previews to a user.

        This removes the role set in the config. This role should be configured
        for every channel where users have link previews. For easy setup, see
        the `rolesetup` command.
        """
        target = await msg_util.get_user_from_mention(ctx.message.mentions,
                                                      user)
        try:
            await restrict.remove_restriction_from_user(target, 'no-preview')
        except discord.errors.Forbidden:
            await self.bot.say("Failed to remove the restriction. Make sure "
                               "the bot has \"Manage Roles\" and the bot's "
                               "role is above the role you want to remove.")
            return
        await self.bot.say("{0.mention} has link previews"
                           "restored.".format(target))
        await log.log('mod', self.bot.channels['mod-logs'], ctx=ctx,
                      target=target, action='Restore Link Previews',
                      action_message='restored link previews to',
                      user=ctx.message.author, reason=reason,
                      emoji='HEAVY LARGE CIRCLE')

    @check.is_staff()
    @commands.command(pass_context=True,
                      description="Remove upload and link previews",
                      brief="Remove upload and link previews from a user",
                      aliases=('noembed',))
    async def rmembed(self, ctx, user, *, reason=''):
        """
        Remove upload permissions and link previews from a user. This is the
        equivalent of using `rmupload` and `rmpreview` at once.

        This notifies the targeted user, including the reason if one is
        provided.

        This applies the roles set in the config for no-upload and no-preview.
        The roles should be configured every channel where users can upload
        files and have link previews. For easy setup, see the `rolesetup`
        command.

        These restrictions persists when the user leaves and re-joins, until it
        is removed with the `resembed` commands for both, or `resupload` and
        `respreview` for the individual restrictions.
        """
        target = await msg_util.get_user_from_mention(ctx.message.mentions,
                                                      user)
        try:
            await restrict.add_restriction_to_user(target, 'no-upload')
            await restrict.add_restriction_to_user(target, 'no-preview')
        except discord.errors.Forbidden:
            await self.bot.say("Failed to add the restrictions. Make sure the "
                               "bot has \"Manage Roles\" and the bot's role "
                               "is above the roles you want to apply.")
            return
        msg = ("You lost upload permissions and link previews from"
               "{0.name}! ".format(self.bot.main_server))
        if reason != "":
            msg += "The given reason is: {0}".format(reason)
        await self.bot.send_message(target, msg)
        await self.bot.say("{0.mention} has lost upload and link"
                           "previews.".format(target))
        await log.log('mod', self.bot.channels['mod-logs'], ctx=ctx,
                      target=target, action='Remove Embed',
                      action_message='removed upload and link previews from',
                      user=ctx.message.author, reason=reason,
                      emoji='CROSS MARK')

    @check.is_staff()
    @commands.command(pass_context=True,
                      description="Restore upload and link previews",
                      brief="Restore upload and link previews to a user")
    async def resembed(self, ctx, user, *, reason=''):
        """
        Restore upload permissions link previews to a user.

        This removes the roles set in the config for no-upload and no-preview.
        The roles should be configured every channel where users can upload
        files and have link previews. For easy setup, see the `rolesetup`
        command.
        """
        target = await msg_util.get_user_from_mention(ctx.message.mentions,
                                                      user)
        try:
            await restrict.remove_restriction_from_user(target, 'no-upload')
            await restrict.remove_restriction_from_user(target, 'no-preview')
        except discord.errors.Forbidden:
            await self.bot.say("Failed to remove the restrictions. Make sure "
                               "the bot has \"Manage Roles\" and the bot's "
                               "role is above the roles you want to remove.")
            return
        await self.bot.say("{0.mention} has upload and link previews"
                           "restored.".format(target))
        await log.log('mod', self.bot.channels['mod-logs'], ctx=ctx,
                      target=target, action='Restore Embed',
                      action_message='restored upload and link previews to',
                      user=ctx.message.author, reason=reason,
                      emoji='HEAVY LARGE CIRCLE')


def setup(bot):
    bot.add_cog(Restrictions(bot))
