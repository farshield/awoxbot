# app

from .awoxbot import AwoxBot
from hello import hello_mod
from stuff import stuff_mod
from market import market_mod
from reddit import reddit_mod


def create_app(post_message):
    """
    Creates an AwoxBot app
    :param post_message: Callback for posting messages
    :return: Reference to an AwoxBot app
    """
    awoxbot_app = AwoxBot(post_message)
    awoxbot_app.register_module(hello_mod)
    awoxbot_app.register_module(stuff_mod)
    awoxbot_app.register_module(market_mod)
    awoxbot_app.register_module(reddit_mod)
    return awoxbot_app
