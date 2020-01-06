import os
import json
import logging
from datetime import datetime


class Scheduler():
    __shared_state = dict()
    __data = dict()
    def __init__(self):
        self.__dict__ = self.__shared_state
        if not self.__data:
            # who are we?
            uid = os.getuid()
            if uid == 0:
                logging.info("Executing as root.")
                self._data_file = "/var/lib/backive/data.json"
            else:
                logging.info("Executing as user.")
                self._data_file = os.path.join(
                    os.path.expanduser("~"),
                    ".config",
                    "backive",
                    "data.json"
                    )
            if not os.path.exists(os.path.dirname(self._data_file)):
                os.makedirs(os.path.dirname(self._data_file))
                self.save()

    def save(self):
        with open(self._data_file, "w") as stream:
            json.dump(self.__data, stream, indent=2)

    def load(self):
        with open(self._data_file, "r") as stream:
            self.__data = json.load(stream)

    def register_backup(self, name, frequency):
        backups = self.__data.get("backups", dict())
        if not backups:
            self.__data["backups"] = backups
        if (
            name not in backups.keys() or
            backups[name] != frequency
            ):
            backups[name] = frequency
        self.save()

    def register_run(self, name):
        runs = self.__data.get("runs", dict())
        if not runs:
            self.__data["runs"] = runs
        if name not in runs.keys():
            runs[name] = [datetime.now().isoformat()]
        else:
            runs[name].append(datetime.now().isoformat())
        self.save()

    def should_run(self, name):
        pass

    def get_overtimed(self):
        return list()
