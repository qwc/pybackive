import os
import backive.config.config as cfg


class Device:
    disks_by_uuid = "/dev/disk/by-uuid"

    def __init__(self, name, config=None):
        self.name = name
        self.config = config

    @classmethod
    def instance(cls, name, config=None):
        return Device(name, config)

    @classmethod
    def get_list(cls):
        if os.path.exists(cls.disks_by_uuid):
            uuids = os.listdir(cls.disks_by_uuid)
            return uuids
        return []

    def mount(self, path):
        pass

    def unmount(self):
        pass

