import os


class Backup:
    def __init__(self, name, cfg=None):
        self.name = name
        self.config = cfg

    def get_frequency(self):
        return self.config.get("frequency", None)

    def run(self):

        if self.config.get("scripts", None):
            pass

