import os
import json
import logging
from datetime import datetime


class Scheduler():
    """
    TODO
    """
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
            else:
                self.load()

    def save(self):
        logging.debug("Scheduler.save()")
        with open(self._data_file, "w") as stream:
            json.dump(self.__data, stream, indent=2)

    def load(self):
        logging.debug("Scheduler.load()")
        if not os.path.exists(os.path.dirname(self._data_file)):
            os.makedirs(os.path.dirname(self._data_file))
            self.save()
        with open(self._data_file, "r") as stream:
            self.__data = json.load(stream)

    def register_backup(self, name, frequency):
        logging.debug("Registering %s, freq %s in Scheduler", name, frequency)
        backups = self.__data.get("backups", dict())
        if not backups:
            self.__data["backups"] = backups
        if (
            name not in backups.keys() or
            backups[name] != frequency
        ):
            backups[name] = frequency
        self.save()

    async def register_run(self, name):
        logging.info("Registered run of backup '%s'", name)
        runs = self.__data.get("runs", dict())
        if not runs:
            self.__data["runs"] = runs
        if name not in runs.keys():
            runs[name] = [datetime.now().isoformat()]
        else:
            runs[name].append(datetime.now().isoformat())
        self.save()

    async def should_run(self, name):
        logging.debug("Checking if %s may run...", name)
        runs = self.__data.get("runs", dict())
        if name not in runs:
            logging.debug("Not registered, so YES")
            return True
        frequency = 0
        if name in runs:
            logging.debug("Registered, checking...")
            backups = self.__data.get("backups", dict())
            if name in backups:
                logging.debug("retrieving frequency")
                frequency = backups[name]
            last_ts = runs[name][-1]
            now = datetime.now()
            last = datetime.fromisoformat(last_ts)
            diff = now - last
            days = diff.days
            if days >= frequency and days >= 1 or frequency == 0:
                logging.debug("YES, should run.")
                return True
        logging.debug("No should not run.")
        return False

    def get_overtimed(self):
        overtime = list()
        now = datetime.now()
        runs = self.__data.get("runs", dict())
        for bkp_name, freq in self.__data.get("backups").items():
            if bkp_name not in runs.keys():
                overtime.append(bkp_name)
            else:
                last_ts = runs[bkp_name][-1]
                last = datetime.fromisoformat(last_ts)
                diff = now - last
                days = diff.days
                if days > freq and freq != 0:
                    overtime.append(bkp_name)
        return overtime
