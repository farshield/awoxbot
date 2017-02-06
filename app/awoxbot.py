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

    def display_reddit_salt(self, content, slack_channel, body_limit):
        """
        Pretty print reddit posts/comments
        :param content: Input tuple containing post/comment data
        :param slack_channel: Slack channel name where data will be sent
        :param body_limit: Limit post/comment body text to a certain number of characters
        :return: None
        """
        display_message = ""
        for item in content:
            item_type = item[0]
            url = item[3]
            author = item[4]
            title = item[5]
            text = item[6]

            if len(text) > body_limit:
                display_message += "*[Text limited to {} chars]* ".format(body_limit)

            if item_type == 'post':
                display_message += "New post `{}` by `{}` - `{}`\n".format(title, author, url)
                if text:
                    display_message += "```{}```\n".format(text[:body_limit])
            elif item_type == 'comment':
                display_message += "New comment by `{}` in `{}` - `{}`\n".format(author, title, url)
                display_message += "```{}```\n".format(text[:body_limit])

        if display_message:
            self.post_message(slack_channel, display_message)

    def monitor_reddit(self):
        """
        Create a new thread where the main reddit listener will execute
        :return: None
        """
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
