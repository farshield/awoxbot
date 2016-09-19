# app

from .awoxbot import AwoxBot
from hello import hello_mod


def create_app(post_message):
    """
    Creates an AwoxBot app
    :param post_message: Callback for posting messages
    :return: Reference to an AwoxBot app
    """
    awoxbot_app = AwoxBot(post_message)
    awoxbot_app.register_module(hello_mod)
    return awoxbot_app
