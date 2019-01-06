import os
import pwd
from ruamel.yaml import YAML
import logging

from backive.core.backup import Backup
from backive.core.device import Device


class Config:

    def __init__(self):
        self._config = dict()

    def find_config(self):
        # who are we?
        uid = os.getuid()
        # name?
        user = pwd.getpwuid(uid).pw_name
        try:
            if uid == 0:
                config_file = "/etc/backive.yml"
            else:
                config_file = os.path.join(os.path.expanduser("~"), ".backive", "backive.yml")
                pass

            with open(config_file, "r") as cfg:
                self._config = YAML().load(cfg)
        except Exception as e:
            logging.error(e)

    def get_devices(self):
        devices = []
        if self._config.get("devices", None):
            data = self._config.get("devices")
            for device in data:
                devices.append(
                    Device.instance(
                        device,
                        data.get(device)
                        )
                    )
        return devices

    def get_backups(self):
        backups = []
        if self._config.get("backups", None):
            data = self._config.get("backups")
            for name in data:
                backups.append(
                    Backup.instance(
                        name,
                        data.get(name)
                        )
                    )
        return backups

    def get_globals(self):
        if self._config.get("defaults", None):
            return self._config.get("defaults")
        return {}
