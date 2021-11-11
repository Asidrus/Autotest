import asyncio
from logging import debug
from time import time, sleep


class Client:

    def __init__(self, ip: str = "192.168.248.32", port: int = 9654, name: dict = {"first_name": "autotest", "last_name": ""}, header: str = "", debug=1):
        self.IP = ip
        self.port = port
        self.name = name
        self.header = header
        self.debug = debug

    def send(self, text, ip=None, port=None):
        asyncio.run(self.asyncSend(text, ip, port))

    async def asyncSend(self, text, ip=None, port=None):
        IP = self.IP if ip is None else ip
        port = self.port if port is None else port
        reader, writer = await asyncio.open_connection(IP, port)
        msg = {"from": self.name, "date": time(), "text": self.header + text, 'debug': self.debug}
        writer.write(str(msg).encode())
        data = await reader.read(2**10)
        print(data)
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    client = Client(debug=0)
    for i in range(1000):
        client.send("дудосю")
        sleep(0.1)