import asyncio
from time import time, sleep

from libs.protocol import Protocol

class Client:
    messages = []

    def __init__(self,
                 ip: str = "localhost",
                 port: int = 1234,
                 name: dict = {"first_name": "autotest", "last_name": ""},
                 header: str = "",
                 debug: int = 1):  # 0 or 1
        self.IP = ip
        self.port = port
        self.name = name
        self.header = header
        self.debug = debug

    def send(self, msg, ip=None, port=None):
        asyncio.run(self.asyncSend(msg, ip, port))

    async def asyncSend(self, msg, ip=None, port=None):
        IP = self.IP if ip is None else ip
        port = self.port if port is None else port
        reader, writer = await asyncio.open_connection(IP, port)
        # writer.write(str(msg).encode())
        writer.write(msg)
        data = await reader.read(2 ** 10)
        print(data)
        writer.close()
        await writer.wait_closed()

    def createMessage(self, text):
        msg = {"from": self.name, "date": time(), "text": self.header + text, 'debug': self.debug}
        self.messages.append(msg)
        return msg


if __name__ == "__main__":
    client = Client(debug=0)
    protocol = Protocol()
    protocol.writeMessage(b'hello', b'world')
    client.send(protocol.raw)
