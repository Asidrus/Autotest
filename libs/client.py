import asyncio
from time import time


class Client:

    IP = None
    port = None
    name = None
    header = None

    def __init__(self, ip: str = "localhost", port: int = 1234, name: dict = {"first_name": "Автотест", "last_name": ""}, header: str = ""):
        print(ip)
        self.IP = ip
        self.port = port
        self.name = name
        self.header = header

    def send(self, text, ip=None, port=None):
        asyncio.run(self.asyncSend(text, ip, port))

    async def asyncSend(self, text, ip=None, port=None):
        IP = self.IP if ip is None else ip
        port = self.port if port is None else port
        reader, writer = await asyncio.open_connection(IP, port)
        print(self.header)
        print(text)
        msg = {"from": self.name, "date": time(), "text": self.header + text}
        writer.write(str(msg).encode())
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    client = Client("localhost", 1234, {"first_name": "Автотест", "last_name": ""}, "")
    client.send("hi", "localhost", 1234)