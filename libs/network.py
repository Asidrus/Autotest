import asyncio
import json
import sys


class Protocol:
    """
    protocol v 0.2.1
    text and image transmission

    @changelog v 0.2
    remove debug
    @changelog v 0.2.1
    add check on stop_reading flag
    if not True return None
    """
    header = [{'head': "request", "data": {"len": 8, "offset": 0, "value": None}},
              {'head': "contentType", "data": {"len": 1, "offset": 8, "value": None}},
              {'head': "content", "data": {"len": 4, "offset": 9, "value": None}},
              {'head': "image", "data": {"len": 8, "offset": 13, "value": None}}]

    raw = b''

    STOP_READING = False
    serial = 0
    data = {}

    def __headerLength__(self):
        count = 0
        for head in self.header:
            count = count + head['data']['len']
        return count

    def __bodyLength__(self):
        length = 0
        for head in self.header:
            if head['head'] != "request":
                length = length + head['data']['value']
        return length

    def set(self, key, value):
        for head in self.header:
            if head['head'] == key:
                head['data']['value'] = value
                return None

    def setData(self, content, contentType: str = 'json', image: bytes = b''):
        if contentType == 'json':
            content = str(content).encode()
            contentType = 0
        elif contentType == 'text':
            content = content.encode()
            contentType = 1
        self.set("contentType", 1)
        self.set("content", len(content))
        self.set("image", len(image))
        self.set("request", self.__headerLength__() + self.__bodyLength__())
        for head in self.header:
            self.raw = self.raw + (head['data']['value']).to_bytes(head['data']['len'], byteorder='big')
        self.raw = self.raw + \
                   contentType.to_bytes(1, byteorder='big') + \
                   content + \
                   image
        return self.raw

    def getData(self, s: bytes):
        for head in self.header:
            offset = head['data']['offset']
            length = head['data']['len']
            self.set(head['head'], int.from_bytes(s[offset:offset + length], 'big'))
        bl = self.__headerLength__()
        cursor = bl
        for head in self.header:
            if head['head'] != 'request':
                length = head['data']['value']
                self.data[head['head']] = s[cursor:cursor + length]
                cursor = cursor + length
        contentType = int.from_bytes(self.data['contentType'], 'big')
        if contentType == 0:
            self.data['contentType'] = 'json'
            self.data['content'] = json.loads(self.data['content'].decode('utf-8').replace("'", "\""))
        elif contentType == 1:
            self.data['contentType'] = 'text'
            self.data['content'] = self.data['content'].decode('utf-8')

    def setChunk(self, chunk):
        if self.serial == 0:
            self.raw = chunk
            offset = self.header[0]['data']['offset']
            length = self.header[0]['data']['len']
            self.header[0]['data']['value'] = int.from_bytes(self.raw[offset:offset + length], 'big')
            self.serial = self.serial + 1
        else:
            self.raw = self.raw + chunk
            self.serial = self.serial + 1
        if len(self.raw) >= self.header[0]['data']['value']:
            self.STOP_READING = True
            self.getData(self.raw)


class Server:
    ip: str = None
    port: int = None
    handler = None

    def __init__(self, ip='localhost', port=1234, handler=None):
        self.ip = ip
        self.port = port
        self.handler = handler

    async def serveClient(self, reader, writer):
        request = await readMessage(reader)
        if request is None:
            print(f'Client unexpectedly disconnected')
        else:
            if self.handler is None:
                pass
            else:
                response = await self.handler(**request)
                if response is not None:
                    await writeMessage(writer, **response)
                writer.close()

    async def runSever(self):
        server = await asyncio.start_server(self.serveClient, self.ip, self.port)
        await server.serve_forever()


class Client:
    handler = None
    ip = None
    port = None

    def __init__(self, ip='localhost', port=1234, handler=None):
        self.ip = ip
        self.port = port
        self.handler = handler

    async def send(self, **kwargs):
        while True:
            try:
                reader, writer = await asyncio.open_connection(self.ip, self.port)
            except Exception as e:
                raise Exception(f'Couldn`t connect to {self.ip}:{self.port}')
            await writeMessage(writer, **kwargs)
            data = await readMessage(reader)
            if self.handler is None:
                writer.close()
                return data
            else:
                res = await self.handler(**data)
                if res == True:
                    writer.close()
                    return True
                elif res == False:
                    continue
                else:
                    writer.close()
                    return False


async def writeMessage(writer, **kwargs):
    protocol = Protocol()
    writer.write(protocol.setData(**kwargs))


async def readMessage(reader) -> dict:
    protocol = Protocol()
    while not protocol.STOP_READING:
        chunk = await reader.read(2 ** 10)
        if not chunk:
            break
        protocol.setChunk(chunk)
    if not protocol.STOP_READING:
        return None
    else:
        return protocol.data


async def handlerIn(**kwargs):
    print(kwargs)
    return {"contentType": "json", "content": {"text": "ok"}}
    # return {"contentType": "json", "content": {"text": "error"}}


async def handlerOut(**kwargs):
    print(kwargs['text'].decode())
    if kwargs['text'].decode() == 'test':
        return {'text': 'ok'}
    else:
        return {'text': 'error'}


if __name__ == "__main__":
    print(sys.argv[1])
    if sys.argv[1] == '1':
        print('start server')
        server = Server(handler=handlerIn)
        loop = asyncio.new_event_loop()
        loop.create_task(server.runSever())
        loop.run_forever()
    else:
        print('start client')
        client = Client()
        asyncio.run(client.send(contentType='text', content='hello world', image=b'adasd'))
