# stuff.py
# -*- coding: utf-8 -*-

import random
import app.utils.upsidedown.upsidedown as upsidedown
from . import stuff_mod


@stuff_mod.register_cmd(r'^!flip')
@stuff_mod.register_cmd(r'^!(coin)?toss')
def cointoss(_):
    coin = "HEADS" if random.randint(1, 100) <= 50 else "TAILS"
    return "The coin landed on: `{}`".format(coin)


@stuff_mod.register_cmd(r'^!roll')
def roll(data):
    cmd = data['text'].split()
    if len(cmd) == 2:
        try:
            result = random.randrange(int(cmd[1]))
        except ValueError:
            return "2nd parameter must be an integer greater than 0"
        else:
            return "You roll: `{}`".format(result)
    else:
        return "Proper usage is: `!roll <number>`"


@stuff_mod.register_cmd(r'^!tableflip')
def tableflip(data):
    cmd = data['text'].split()
    if len(cmd) == 1:
        return u'(╯°□°）╯︵ ┻━┻'
    else:
        return u'（╯°□°）╯︵ {}'.format(upsidedown.transform(" ".join(cmd[1:])))


@stuff_mod.register_cmd(r'^!insult')
def insult(data):
    pass
