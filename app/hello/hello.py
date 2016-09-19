# hello.py

from . import hello_mod


@hello_mod.register_cmd(r'(hello|hi|hey) awoxbot')
def hello_world(data):
    return 'Hello <@{}>!'.format(data['user'])
