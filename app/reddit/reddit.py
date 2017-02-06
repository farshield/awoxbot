"""
Reddit to Slack Plugin
"""
import os
from app.utils.redditm.redditm import RedditM
from . import reddit_mod

reddit_config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reddit.conf')
redditm = RedditM(reddit_config_file)


@reddit_mod.register_init
def reddit_init():
    redditm.monitor_reddit(display_reddit_salt)


@reddit_mod.register_cmd(r'^!reddit (conf|info)')
def reddit_config_file(data):
    cmd = data['text'].split()
    if cmd[1] == 'conf':
        display_message = "Reddit monitor config: ```{}```".format(str(redditm.config_data))
    else:
        display_message = '```number of successful requests = {}\n'.format(redditm.requests_ok)
        display_message += 'number of failed requests = {}\n'.format(redditm.requests_error)
        display_message += 'last post ID read = {}\n'.format(redditm.last_post_id)
        display_message += 'last comment ID read = {}```'.format(redditm.last_comment_id)
    return display_message


def display_reddit_salt(content):
    """
    Pretty print reddit posts/comments
    :param content: Input tuple containing post/comment data
    :param slack_channel: Slack channel name where data will be sent
    :param body_limit: Limit post/comment body text to a certain number of characters
    :return: None
    """
    slack_channel = redditm.config_data['slack_channel']
    body_limit = redditm.config_data['body_limit']
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
