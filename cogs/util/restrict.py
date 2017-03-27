import json


def add_restriction(user_id, role_key):
    with open("data/restrictions.json", "r") as f:
        rsts = json.load(f)
    if user_id not in rsts:
        rsts[user_id] = []
    if role_key not in rsts[user_id]:
        rsts[user_id].append(role_key)
        with open("data/restrictions.json", "w") as f:
            json.dump(rsts, f)
