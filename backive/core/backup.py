import os
import logging


class Backup:
    def __init__(self, name, cfg=None):
        self.name = name
        self.config = cfg

    @classmethod
    def instance(cls, name, config=None):
        logging.debug("Backup instance created (%s)", name)
        return Backup(name, config)

    def get_frequency(self):
        return self.config.get("frequency", None)

    def run(self):
        if self.config.get("scripts", None):
            pass

