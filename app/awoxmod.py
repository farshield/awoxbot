# awoxmod.py


class AwoxMod:
    """
    Command Registry for AwoxBot Modules
    """
    def __init__(self, mod_name):
        self.mod_name = mod_name
        self.command_map = {}
        self.app = None

    def talk(self, channel, message):
        if self.app:
            return self.app.post_message(channel, message)

    def register_cmd(self, name):
        """
        Decorator for registering a command for the current module
        :param name: RegEx pattern
        :return:
        """
        def func_wrapper(func):
            self.command_map[name] = func
            return func
        return func_wrapper
