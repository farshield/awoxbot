# awoxbot.py

import re


class AwoxBot:
    """
    Command Dispatcher for AwoxBot
    """
    def __init__(self, post_message):
        self.post_message = post_message  # callback
        self.module_list = []

    def register_module(self, module):
        module.app = self
        self.module_list.append(module)

    def process_command(self, channel, user, text):
        for module in self.module_list:
            for command in module.command_map:
                if re.search(command, text, re.IGNORECASE):
                    callback = module.command_map[command]
                    if callable(callback):
                        return callback(channel, user, text)


def main():
    from app import create_app

    def post_message(channel, message):
        print('[{}] {}'.format(channel, message))

    awoxbot = create_app(post_message)

    while True:
        command = raw_input('> ')
        if not command:
            break
        awoxbot.process_command('DEBUG', None, command)

if __name__ == "__main__":
    main()
