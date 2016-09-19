# hello.py

from . import hello_mod


@hello_mod.register_cmd(r'(hello|hi|hey) awoxbot')
def hello_world(channel, user, _):
    hello_mod.talk(channel, 'Hello <@{}>!'.format(user))
