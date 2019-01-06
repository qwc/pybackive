import os
import pwd
from ruamel.yaml import YAML
import logging


class Config:

    def __init__(self):
        pass

    def find_config(self):
        # who are we?
        uid = os.getuid()
        # name?
        user = pwd.getpwuid(uid).pw_name
        try:
            if uid == 0:
                config_file = "/etc/mbd.yml"
            else:
                config_file = os.path.join(os.path.expanduser("~"), ".mbd", "mbd.yml")
                pass

            with open(config_file, "r") as cfg:
                self._config = YAML().load(cfg)
        except Exception as e:
            logging.error(e)
