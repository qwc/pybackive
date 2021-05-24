import os


AVAILABLE_TOOLS = {}

def register_tool(name):
    """
    TODO
    """
    def decorator(Cls):
        AVAILABLE_TOOLS.update({name: Cls})
    return decorator


class Tool:
    def __init__(self, options):
        pass

    @classmethod
    def instance(cls, name, options):
        if name in AVAILABLE_TOOLS:
            return AVAILABLE_TOOLS.get(name)(options)
        return None
