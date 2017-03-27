import discord
from discord.ext import commands
from time import tzname, localtime
from . import msg_util
# bot is imported here since ctx isn't always available
from __main__ import logs, bot


async def log(type, *channels, action=None, action_message=None, ctx=None,
              user=None, target=None, emoji=None, reason=None):
    msg = ""
    if type == 'join':
        msg += "{0}**Join**: {1.mention} | {2}\n".format(
            msg_util.emoji('WHITE HEAVY CHECK MARK'), target,
            msg_util.escape_markdown(target)
        )
        msg += "{0}__Creation__: {1.created_at} UTC\n".format(
            msg_util.emoji('SPIRAL CALENDAR PAD'), target
        )
        if logs.APPEND_USER_ID:
            msg += "{0}__User ID__: {1.id}".format(
                msg_util.emoji('LABEL'), target
            )
    elif type == 'leave':
        msg += "{0}**Leave**: {1.mention} | {2}\n".format(
            msg_util.emoji('LEFTWARDS BLACK ARROW'), target,
            msg_util.escape_markdown(target)
        )
        if logs.APPEND_USER_ID:
            msg += "{0}__User ID__: {1.id}".format(
                msg_util.emoji('LABEL'), target
            )
    elif type == 'mod':
        msg += "{0}**{1}**: ".format(msg_util.emoji(emoji), action)
        if user:
            msg += "{0.mention} ".format(user)
        if action_message:
            msg += action_message + ' '
        if target:
            msg += "{0.mention} ".format(target)
            if isinstance(target, discord.User):
                msg += "|| " + format(msg_util.escape_markdown(target))
        if reason:
            msg += "\n{0}__Reason__: {1}".format(msg_util.emoji('PENCIL'), reason)
    bot.debug("Log message:\n  {}".format(msg.strip().replace('\n', '\n  ')))
    for channel in channels:
        await bot.send_message(channel, msg)
