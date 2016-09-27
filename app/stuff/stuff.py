# stuff.py
# -*- coding: utf-8 -*-

import random
import requests
import re
import app.utils.upsidedown.upsidedown as upsidedown
from . import stuff_mod

ROLL_REP_MAX = 16
ROLL_INTERVAL = 10000


@stuff_mod.register_cmd(r'^!flip')
@stuff_mod.register_cmd(r'^!(coin)?toss')
def cointoss(data):
    coin = "HEADS" if random.randint(1, 100) <= 50 else "TAILS"
    return "<@{}>, the coin landed on: `{}`".format(data['user'], coin)


@stuff_mod.register_cmd(r'^!roll')
def roll(data):
    cmd = data['text'].split()
    if len(cmd) == 2:
        rolls = []

        try:
            result = re.match(r'^([0-9]+)d([0-9]+)$', cmd[1], re.IGNORECASE)
            reps = int(result.group(1)) if result else 1
            max_roll = int(result.group(2)) if result else int(cmd[1])

            if 1 <= reps <= ROLL_REP_MAX and max_roll <= ROLL_INTERVAL:
                for _ in xrange(reps):
                    rolls.append(random.randint(1, max_roll))
        except ValueError:
            rolls = []

        if rolls:
            if len(rolls) > 1:
                return '<@{}>, you roll: `{} = {}`'.format(data['user'], ' + '.join(str(x) for x in rolls), sum(rolls))
            else:
                return '<@{}>, you roll: `{}`'.format(data['user'], rolls[0])

    return "Usage: `!roll X` or `!roll AdX`, where `A` and `X` are integers greater than `0`" \
           " and `A <= {}`, `X <= {}`".format(ROLL_REP_MAX, ROLL_INTERVAL)


@stuff_mod.register_cmd(r'^!tableflip')
def tableflip(data):
    cmd = data['text'].split()
    if len(cmd) == 1:
        return u'(╯°□°）╯︵ ┻━┻'
    else:
        return u'（╯°□°）╯︵ {}'.format(upsidedown.transform(" ".join(cmd[1:])))


@stuff_mod.register_cmd(r'^!insult')
def insult(data):
    message = ""
    cmd = data['text'].split()
    try:
        result = requests.get(
            url='http://quandyfactory.com/insult/json',
            timeout=3
        )
    except requests.exceptions.RequestException:
        return 'I have somehow lost the ability to insult people'
    if result.status_code != 200:
        return 'My insult generator is broken :('

    if cmd[1:]:
        message = "{}: ".format(" ".join(cmd[1:]))
    return message + result.json()['insult']
