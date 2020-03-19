import os
import pwd
import json
from ruamel.yaml import YAML
import logging
import jsonschema

class RegularUserException(Exception):
    pass

class Config:
    __shared_state = dict()
    _config = dict()

    def __init__(self):
        self.__dict__ = self.__shared_state
        if not self._config:
            logging.info("Loading configuration...")
            self._schema = dict()
            self._backups = list()
            self._devices = dict()
            file_path = os.path.realpath(__file__)
            schema_path = os.path.join(
                    os.path.dirname(
                        file_path
                    ),
                    "schema.yml"
                )
            with open(schema_path, "r") as stream:
                self._schema = YAML().load(stream)
            self.find_config()

    def find_config(self):
        # who are we?
        uid = os.getuid()
        # name?
        user = pwd.getpwuid(uid).pw_name
        logging.debug("Trying to find the configuration")
        try:
            if uid == 0:
                config_file = "/etc/backive.yml"
            else:
                raise RegularUserException(
                    """
                    It is planned to add functionality to use this service
                    as a regular user, but for the time being it is advised to
                    execute this service as root, because this feature is still
                    planned and needs more development time.
                    """)
                config_file = os.path.join(
                    os.path.expanduser("~"),
                    ".config",
                    "backive",
                    "backive.yml"
                )

            with open(config_file, "r") as cfg:
                self._config = YAML().load(cfg)
            logging.debug(
                "Found config: %s\n%s",
                config_file,
                json.dumps(self._config, indent=4)
            )
            jsonschema.validate(self._config, self._schema)
        except RegularUserException as e:
            raise e
        except Exception as e:
            logging.error(e)

    def get_devices(self):
        from backive.core.device import Device
        if self._config.get("devices", None) and not self._devices:
            data = self._config.get("devices")
            for device, values in data.items():
                self._devices.update({
                    device:
                    Device.instance(
                        device,
                        values
                        )
                    })
        return self._devices

    async def get_device(self, name):
        for device, value in self.get_devices().items():
            if device == name:
                return value
        return None

    def get_backups(self) -> list:
        from backive.core.backup import Backup
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

    async def get_uuid_device(self, uuid):
        logging.debug("get device %s", uuid)
        for device, value in self.get_devices().items():
            logging.debug(
                "device %s, config %s", device, json.dumps(value.config)
            )
            if value.config.get("uuid") == uuid:
                return value
        return None

    async def get_backups_by_device(self, uuid):
        name = None
        if not self._config.get("devices"):
            return None
        for k, v in self._config.get("devices").items():
            if v.get("uuid") == uuid:
                name = k
        if name:
            return self.get_device_backups(name)
        return None

    def get_device_backups(self, name):
        backups = list()
        for backup in self.get_backups():
            if backup.config.get("target_device") == name:
                backups.append(backup)
        return backups

    async def get_preferences(self):
        if self._config.get("preferences", None):
            return self._config.get("preferences")
        return {}
