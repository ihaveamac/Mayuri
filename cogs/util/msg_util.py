import unicodedata
from __main__ import logs

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


def get_user_from_mention(mentions, raw_mention):
    for member in mentions:
        if member.mention == raw_mention:
            return member
    return None
