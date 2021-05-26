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
    
    async def _read_stream(self, stream, cb):
        while True:
            line = await stream.readline()
            if line:
                cb(line)
            else:
                break
    
    async def stream_subprocess(self, cmd, environ, outcb, errcb):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=environ
        )

        await asyncio.wait([
            self._read_stream(proc.stdout, outcb),
            self._read_stream(proc.stderr, errcb)
        ])

        return await proc.wait()

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
            backup_env["BACKIVE_TARGET_DIR"] = os.path.join(
                (await Config().get_preferences()).get("mount_root"),
                (await Config().get_device(
                    self.config.get("target_device")
                )).config.get("mountname"),
                self.config.get("to")
            )
            proc = await self.stream_subprocess(
                """mkdir -p {}""".format( backup_env["BACKIVE_TARGET_DIR"]),
                backup_env,
                lambda x: logging.debug("STDOUT: %s", x),
                lambda x: logging.debug("STDERR: %s", x),
            )
#            proc = await asyncio.create_subprocess_shell(
#                """mkdir -p {}""".format( backup_env["BACKIVE_TARGET_DIR"]
#                ),
#                stdout=asyncio.subprocess.PIPE,
#                stderr=asyncio.subprocess.PIPE,
#            )
#            stdout, stderr = await proc.communicate()
#            logging.debug("stdout: %s", stdout.decode())
#            logging.debug("stderr: %s", stderr.decode())
            user = self.config.get("user")
#            proc = await asyncio.create_subprocess_shell(
            proc = await self.stream_subprocess(
#                "set -x; chown -R {} ${{BACKIVE_MOUNT}}/${{BACKIVE_TO}};".format(user) +
#                "sudo -E -u {} sh -c '".format(user) +
                self.config.get("script"),
                backup_env,
                lambda x: logging.debug("STDOUT: %s", x),
                lambda x: logging.debug("STDERR: %s", x),
            )
#                "'",
#                stdout=asyncio.subprocess.PIPE,
#                stderr=asyncio.subprocess.PIPE,
#                shell=True,
#                env=backup_env
#            )
#            stdout, stderr = await proc.communicate()
#            logging.debug("stdout: %s", stdout.decode())
#            logging.debug("stderr: %s", stderr.decode())
            return "done"
