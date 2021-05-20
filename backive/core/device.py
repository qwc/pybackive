import os
import logging
import asyncio
import backive.config.config as cfg


class Device:
    disks_by_uuid = "/dev/disk/by-uuid"

    def __init__(self, name, config=None):
        self.name = name
        self.config = config
        self._mount_dir = None

    @classmethod
    def instance(cls, name, config=None):
        logging.debug("Device instance created (%s)", name)
        return Device(name, config)

    @classmethod
    def get_list(cls):
        if os.path.exists(cls.disks_by_uuid):
            uuids = os.listdir(cls.disks_by_uuid)
            return uuids
        return []

    async def mount(self, path):
        self._mount_dir = os.path.join(path, self.config.get("mountname"))
        dev_path = os.path.join(self.disks_by_uuid, self.config.get("uuid"))
        logging.debug("dev: %s ;; mount: %s", dev_path, self._mount_dir)
        # TODO: use mkdir as indicator for correct access rights (when backive
        # is run as user!)
        proc = await asyncio.create_subprocess_shell(
            """set -x; mkdir -p {mountpoint}
mount -v -o users,noexec {dev_path} {mountpoint}""".format(
                mountpoint=self._mount_dir,
                dev_path=dev_path,
            ),
            shell=True,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        logging.debug("stdout: %s", stdout.decode())
        logging.debug("stderr: %s", stderr.decode())
        # TODO: Also add a touch operation in the target mount if the correct
        # access rights are given! (when backive is run as user)
        return True # on success, False on failure

    async def unmount(self):
        if not self._mount_dir:
            return
        proc = await asyncio.create_subprocess_shell(
            """sync
sudo umount -v %s
""" % self._mount_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        logging.debug("stdout: %s", stdout.decode())
