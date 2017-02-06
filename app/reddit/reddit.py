"""
Reddit to Slack Plugin
"""
import threading
from app.utils.redditm import redditm
from . import reddit_mod


@reddit_mod.register_init
def reddit_init():
    monitor_reddit()


def display_reddit_salt(content, slack_channel, body_limit):
    """
    Pretty print reddit posts/comments
    :param content: Input tuple containing post/comment data
    :param slack_channel: Slack channel name where data will be sent
    :param body_limit: Limit post/comment body text to a certain number of characters
    :return: None
    """
    display_message = u""
    for item in content:
        item_type = item[0]
        url = item[3]
        author = item[4]
        title = item[5]
        text = item[6]

        if len(text) > body_limit:
            display_message += u"*[Text limited to {} chars]* ".format(body_limit)

        if item_type == 'post':
            display_message += u"New post `{}` by `{}` - `{}`\n".format(title, author, url)
            if text:
                display_message += u"```{}```\n".format(text[:body_limit])
        elif item_type == 'comment':
            display_message += u"New comment by `{}` in `{}` - `{}`\n".format(author, title, url)
            display_message += u"```{}```\n".format(text[:body_limit])

    if display_message:
        reddit_mod.talk(slack_channel, display_message)


def monitor_reddit():
    """
    Create a new thread where the main reddit listener will execute
    :return: None
    """
    reddit_thread = threading.Thread(target=redditm.reddit_main, args=(display_reddit_salt,))
    reddit_thread.daemon = True
    reddit_thread.start()
