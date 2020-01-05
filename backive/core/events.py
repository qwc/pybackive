import os
import asyncio


class EventInterface:
    def __init__(self, event_callback, unix_socket_path=None, loop=None):
        self.event_callback = event_callback
        if not unix_socket_path:
            unix_socket_path = "/tmp/backive/backive.sock"
        if not os.path.exists(os.path.dirname(unix_socket_path)):
            os.makedirs(os.path.dirname(unix_socket_path))
        try:
            os.remove(unix_socket_path)
        except OSError:
            pass
        if not loop:
            loop = asyncio.get_event_loop()
        loop.create_task(asyncio.start_unix_server(self.client_connected, unix_socket_path))

    async def client_connected(self, reader, writer):
        print("client_connected")
        data = None
        data = (await reader.read()).decode('utf8')
        await self.event_callback(data)


