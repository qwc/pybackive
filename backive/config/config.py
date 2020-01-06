import logging
import os
import pwd
from ruamel.yaml import YAML
import logging
import jsonschema

from backive.core.backup import Backup
from backive.core.device import Device


class Config:
    __shared_state = dict()
    _config = dict()

    def __init__(self):
        self.__dict__ = self.__shared_state
        if not self._config:
            logging.info("Loading configuration...")
            self._schema = dict()
            self._backups = list()
            self._devices = list()
            file_path = os.path.realpath(__file__)
            schema_path = os.path.join(
                    os.path.dirname(
                        file_path
                    ),
                    "schema.yml"
                )
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
        if self._config.get("devices", None) and not self._devices:
            data = self._config.get("devices")
            for device in data:
                self._devices.append(
                    Device.instance(
                        device,
                        data.get(device)
                        )
                    )
        return self._devices

    def get_backups(self):
        if self._config.get("backups", None) and not self._backups:
            data = self._config.get("backups")
            for name in data:
                self._backups.append(
                    Backup.instance(
                        name,
                        data.get(name)
                        )
                    )
        return self._backups

    def get_backups_by_device(self, uuid):
        name = None
        for k, v in self._config.get("devices").items():
            if v.get("uuid") == uuid:
                name = k
        if name:
            return self.get_device_backups(name)
        return None

    def get_device_backups(self, name):
        backups = list()
        for backup in self.get_backups():
            if backup.target == name:
                backups.append(backup)
        return backups

    def get_preferences(self):
        if self._config.get("preferences", None):
            return self._config.get("preferences")
        return {}
