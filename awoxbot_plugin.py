# awoxbot_plugin.py

from app import create_app

crontable = []
outputs = []


def post_message(channel, message):
    """
    Sends a message to a specified Slack channel
    :param channel: Slack channel
    :param message: Message to be sent
    :return:
    """
    if message:
        outputs.append([channel, message])

awoxbot = create_app(post_message)


def process_hello(_):
    """
    Event - connected to server
    :param _:
    :return:
    """
    print("[Info] AwoxBot connected to server")


def process_message(data):
    """
    Event - message received
    :param data:
    :return:
    """
    awoxbot.process_command(data)
