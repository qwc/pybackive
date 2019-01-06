import os


class Backup:

    config = {}

    def __init__(self, name, cfg=None):
        pass

    def run(self):
        pass

    @classmethod
    def instance(cls, name, cfg):
        return Backup(name, cfg)
