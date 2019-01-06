from ruamel.yaml import YAML
import logging
import sys
import signal
import os
import pwd


logging.basicConfig(format='%(asctime)s->%(name)s@%(levelname)s: %(message)s', filename=sys.stdout, level=logging.INFO)

got_signal = False
disks_by_uuid = "/dev/disk/by-uuid"


class MBD:
    def __init__(self):
        self._config = None
        # who are we?
        uid = os.getuid()
        # name?
        user = pwd.getpwuid(uid).pw_name
        try:
            if uid == 0:
                config_file = "/etc/mbd.yml"
            else:
                config_file = os.path.join(os.path.expanduser("~"), ".mbd", "mbd.yml")
                pass

            with open(config_file, "r") as cfg:
                self._config = YAML().load(cfg)
        except Exception as e:
            logging.error(e)

    def get_list_of_devices(self):
        if os.path.exists(disks_by_uuid):
            uuids = os.listdir(disks_by_uuid)
            return uuids
        return []

    def get_backup_list(self):
        defaults = self._config.get("defaults", None)
        if defaults:
            mount_root = defaults.get("mount_root", "/media")
        else:
            mount_root = "/media"

        devices = self._config.get("devices", dict())
        for d in devices:
            if d in self.get_list_of_devices():
                # do backup to this device
                # mount it
                mount = os.path.join(mount_root, devices[d].get("mountname"))
                os.system("mount {byuuid}/{uuid} {mount}".format(
                    byuuid=disks_by_uuid, uuid=d, mount=mount))
                last_backup_file = os.path.join(mount, devices[d].get("backup").get("target"), ".mdb.last")
                if os.path.exists(last_backup_file):
                    with open(last_backup_file, "r") as f:
                        last_backup = f.read()






def signal_handler(signum, frame):
    got_signal = True


signal.signal(signal.SIGHUP, signal_handler)

if __name__ == "__main__":
    pass
