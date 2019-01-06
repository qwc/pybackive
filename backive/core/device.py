import os


class Device:
    disks_by_uuid = "/dev/disk/by-uuid"

    def __init__(self):
        pass

    @classmethod
    def get_device_list(cls):
        if os.path.exists(cls.disks_by_uuid):
            uuids = os.listdir(cls.disks_by_uuid)
            return uuids
        return []
