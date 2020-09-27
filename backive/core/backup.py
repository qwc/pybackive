import os
import logging
from subprocess import Popen
import asyncio
from backive.config.config import Config


class Backup:
    def __init__(self, name, cfg=None):
        self.name = name
        self.config = cfg

    @classmethod
    def instance(cls, name, config=None):
        logging.debug("Backup instance created (%s)", name)
        return Backup(name, config)

    def get_frequency(self):
        return self.config.get("frequency", None)

    async def run(self):
        logging.debug("Running backup %s", self.name)
        if self.config.get("script", None) is not None:
            logging.debug("Executing script..")
            backup_env = os.environ.copy()
            backup_env["BACKIVE_FROM"] = self.config.get("from")
            backup_env["BACKIVE_TO"] = self.config.get("to")
            backup_env["BACKIVE_MOUNT"] = os.path.join(
                (await Config().get_preferences()).get("mount_root"),
                (await Config().get_device(
                    self.config.get("target_device")
                )).config.get("mountname")
            )
            proc = await asyncio.create_subprocess_shell(
                """mkdir -p {}""".format(
                    os.path.join(
                        backup_env["BACKIVE_MOUNT"],
                        backup_env["BACKIVE_TO"]
                    )
                ),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            logging.debug("stdout: %s", stdout)
            logging.debug("stderr: %s", stderr.decode())
            user = self.config.get("user")
            proc = await asyncio.create_subprocess_shell(
#                "set -x; chown -R {} ${{BACKIVE_MOUNT}}/${{BACKIVE_TO}};".format(user) +
#                "sudo -E -u {} sh -c '".format(user) + 
                self.config.get("script"),
#                "'",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True,
                env=backup_env
            )
            stdout, stderr = await proc.communicate()
            logging.debug("stdout: %s", stdout.decode())
            logging.debug("stderr: %s", stderr.decode())
            return stdout
