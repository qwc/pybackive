import os
import pwd
from ruamel.yaml import YAML
import logging
import jsonschema

from backive.core.backup import Backup
from backive.core.device import Device


class Config:

    def __init__(self):
        self._config = dict()
        self._schema = dict()
        file_path = os.path.realpath(__file__)
        schema_path = os.path.join(file_path, "schema.yml")
        with open(schema_path, "r") as stream:
            self._schema = YAML().load(stream)

    def find_config(self):
        # who are we?
        uid = os.getuid()
        # name?
        user = pwd.getpwuid(uid).pw_name
        try:
            if uid == 0:
                config_file = "/etc/backive.yml"
            else:
                config_file = os.path.join(
                    os.path.expanduser("~"),
                    ".config",
                    "backive",
                    "backive.yml"
                )

            with open(config_file, "r") as cfg:
                self._config = YAML().load(cfg)
            jsonschema.validate(self._config, self._schema)
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

    def get_device_backups(self, device):
        uuid = device
        device_name = self._config.get("devices").get(uuid).get("name")
        backups = []
        for backup in self.get_backups():
            if backup.target == uuid or backup.target == device_name:
                backups.append(backup)
        return backups

    def get_preferences(self):
        if self._config.get("preferences", None):
            return self._config.get("preferences")
        return {}
