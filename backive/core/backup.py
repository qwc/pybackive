import os
import logging
from subprocess import Popen
import asyncio


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
        if self.config.get("scripts", None) is not None:
            logging.debug("Executing script..")
            proc = await asyncio.create_subprocess_shell(
                self.config.get("script"),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            logging.debug("stdout: %s", stdout)
            return stdout
