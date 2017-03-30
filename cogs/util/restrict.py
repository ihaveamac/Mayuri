import discord
import json
# bot is imported here since ctx/bot isn't always available through other means
from __main__ import bot


async def add_restriction_to_user(user, role_key):
    if role_key not in bot.roles:
        raise KeyError("role key `{0}' not found".format(role_key))
    if not isinstance(user, discord.User):
        if isinstance(user, str):
            user_id = user
        else:
            raise TypeError("target must be a User or string with user ID")
    else:
        user_id = user.id
        await bot.add_roles(user, bot.roles[role_key])
    with open("data/restrictions.json", "r") as f:
        rsts = json.load(f)
    if user_id not in rsts:
        rsts[user_id] = []
    if role_key not in rsts[user_id]:
        rsts[user_id].append(role_key)
        with open("data/restrictions.json", "w") as f:
            json.dump(rsts, f)


async def remove_restriction_from_user(user, role_key):
    if role_key not in bot.roles:
        raise KeyError("role key `{0}' not found".format(role_key))
    if not isinstance(user, discord.User):
        if isinstance(user, str):
            user_id = user
        else:
            raise TypeError("target must be a User or string with user ID")
    else:
        user_id = user.id
        await bot.remove_roles(user, bot.roles[role_key])
    with open("data/restrictions.json", "r") as f:
        rsts = json.load(f)
    if user_id not in rsts:
        rsts[user_id] = []
    if role_key in rsts[user_id]:
        rsts[user_id].remove(role_key)
        with open("data/restrictions.json", "w") as f:
            json.dump(rsts, f)
