import unittest
import os
import asyncio
from backive.core.events import EventInterface



class TestEvents(unittest.TestCase):
    def set_data(self, data):
        self.data = data

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.srv_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.socket_path = "/" + os.path.join(
            "tmp",
            "backive",
            "tests"
            )
        if not os.path.exists(os.path.dirname(self.socket_path)):
            os.makedirs(os.path.dirname(self.socket_path))
        self.eventif = EventInterface(self.set_data, self.socket_path, self.srv_loop)
        self.data = None
        pass

    def tearDown(self):
        pass

    def testEventInput(self):
        async def test():
            reader, writer = await asyncio.open_unix_connection(self.socket_path)
            writer.write("hello world".encode('utf8'))
            await writer.drain()
            writer.close()
        self.loop.run_until_complete(test())
        self.srv_loop.run_until_complete()
        self.assertEqual(self.data, "hello world")

        pass
