import os


class Backup:
    def __init__(self, name, cfg=None):
        self.name = name
        self.config = cfg

    def run(self):
        pass

    @classmethod
    def instance(cls, name, cfg):
        return Backup(name, cfg)
