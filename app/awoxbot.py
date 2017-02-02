# awoxbot.py

import threading
import re
from utils.reddit import reddit


class AwoxBot:
    """
    Command Dispatcher for AwoxBot
    """
    def __init__(self, post_message):
        self.post_message = post_message  # callback
        self.module_list = []
        self.reddit_channel = None
        self.reddit_limit = 3072  # number of characters in one post

    def register_module(self, module):
        module.app = self
        self.module_list.append(module)

    def process_command(self, data):
        for module in self.module_list:
            for command in module.command_map:
                # try to find matching command
                if re.search(command, data['text'], re.IGNORECASE):
                    callback = module.command_map[command]
                    if callable(callback):
                        self.post_message(data['channel'], callback(data))

    def display_reddit_salt(self, content):
        display_message = ""

        for item in content:
            # post_data = ('post', post_id, created, permalink, author, post_title, text)
            item_type = item[0]
            url = item[3]
            author = item[4]
            title = item[5]
            text = item[6]

            if len(text) > self.reddit_limit:
                display_message += "*[Text limited to {} chars]* ".format(self.reddit_limit)

            if item_type == 'post':
                display_message += "New post `{}` by `{}` - `{}`\n".format(title, author, url)
                display_message += "```{}```\n".format(text[:self.reddit_limit])
            elif item_type == 'comment':
                display_message += "New comment by `{}` in `{}` - `{}`\n".format(author, title, url)
                display_message += "```{}```\n".format(text[:self.reddit_limit])

        if display_message:
            self.post_message(self.reddit_channel, display_message)

    def monitor_reddit(self):
        self.reddit_channel = reddit.reddit_channel_name()
        reddit_thread = threading.Thread(target=reddit.reddit_main, args=(self.display_reddit_salt,))
        reddit_thread.daemon = True
        reddit_thread.start()


def main():
    from app import create_app

    def post_message(channel, message):
        print('[{}] {}'.format(channel, message))

    awoxbot = create_app(post_message)

    while True:
        command = raw_input('> ')
        if not command:
            break
        awoxbot.process_command({'channel': 'Debug', 'user': None, 'text': command})

if __name__ == "__main__":
    main()
