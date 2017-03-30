import unicodedata
# bot is imported here since ctx/bot isn't always available through other means
from __main__ import logs, bot

# http://stackoverflow.com/questions/3411771/multiple-character-replace-with-python
chars = "\\`*_<>#@:~"


def escape_markdown(text):
    text = str(text)
    for c in chars:
        if c in text:
            text = text.replace(c, "\\" + c)
    return text.replace("@", "@\u200b")  # prevent mentions


def emoji(text, force=False):
    if logs.USE_EMOJI or force:
        if text:
            if len(text) > 1:
                try:
                    unicode_char = unicodedata.lookup(text)
                except KeyError:
                    unicode_char = '\N{BLACK QUESTION MARK ORNAMENT}'
                return unicode_char + ' '
            else:
                return text + ' '
        else:
            return '\N{WHITE QUESTION MARK ORNAMENT} '
    else:
        return ""


async def get_user_from_mention(mentions, raw_mention, none_if_fail=False):
    for member in mentions:
        if member.mention == raw_mention:
            return member
    if none_if_fail:
        return None
    else:
        if raw_mention[0:2] == '<@':
            await bot.say("This member is not in the server.")
        elif raw_mention[0] == '@':
            await bot.say("A member was not properly mentioned. Make"
                          "sure the target is in this server.")
        else:
            await bot.say("No member was mentioned.")
        raise KeyError("{0} does not resolve to a user".format(raw_mention))
