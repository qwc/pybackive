import os
import socket


class EventInterface:
    def __init__(self, unix_socket=None):
        if not unix_socket:
            unix_socket = "/tmp/backive/backive.sock"
        self.socket = socket.socket(
                socket.AF_UNIX,
                socket.SOCK_STREAM
                )
        try:
            os.remove(unix_socket)
        except OSError:
            pass
        self.socket.bind(unix_socket)
        self.socket.listen()

    def accept(self):
        return self.socket.accept()



