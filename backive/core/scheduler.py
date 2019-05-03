import os
import json


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Scheduler(metaclass=Singleton):
    def __init__(self):
        self._data = dict()
        # who are we?
        uid = os.getuid()
        if uid == 0:
            self._data_file = "/var/lib/backive/data.json"
        else:
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
            json.dump(self._data, stream, indent=2)

    def load(self):
        with open(self._data_file, "r") as stream:
            self._data = json.load(stream)

    def register_backup(self, name, frequency):
        pass

    def register_run(self, name):
        pass

    def should_run(self, name):
        pass

    def get_overtimed(self):
        return list()
