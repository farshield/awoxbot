# awoxmod.py


class AwoxMod:
    """
    Command Registry for AwoxBot Modules
    """
    def __init__(self, mod_name):
        self.mod_name = mod_name
        self.command_map = {}
        self.app = None
        self.mod_init = lambda: None

    def talk(self, channel, message):
        if self.app:
            return self.app.post_message(channel, message)

    def register_init(self, func):
        """
        Decorator for registering a command for initializing the module
        :param func: Init callback
        :return:
        """
        self.mod_init = func

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
