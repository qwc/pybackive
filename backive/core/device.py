import os
import backive.config.config as cfg


class Device:
    disks_by_uuid = "/dev/disk/by-uuid"

    def __init__(self, uuid, config=None):
        self.uuid = uuid
        self.config = config

    @classmethod
    def instance(cls, uuid, config):
        return Device(uuid, config)

    @classmethod
    def get_list(cls):
        if os.path.exists(cls.disks_by_uuid):
            uuids = os.listdir(cls.disks_by_uuid)
            return uuids
        return []

    def mount(self):
        pass

    def unmount(self):
        pass

