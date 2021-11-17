import asyncio
import json

counter = 0

from libs.protocol import Protocol

async def serve_client(reader, writer):
    global counter
    cid = counter
    counter += 1  # Потоко-безопасно, так все выполняется в одном потоке
    print(f'Client #{cid} connected')

    request = await read_request(reader)
    print(request)
    if request is None:
        print(f'Client #{cid} unexpectedly disconnected')
    else:
        await write_response(writer, request, cid)


# async def read_request(reader, delimiter=b'#END'):
#     request = bytearray()
#     while True:
#         chunk = await reader.read(2 ** 10)
#         if not chunk:
#             # Клиент преждевременно отключился.
#             break
#         request += chunk
#         try:
#             data = json.loads(request.decode("utf-8").replace("'", "\""))
#             return data
#         except:
#             pass
#     return None


async def read_request(reader, delimiter=b'#END'):
    protocol = Protocol()
    while not Protocol.STOP_READING:
        chunk = await reader.read(2 ** 10)
        if not chunk:
            # Клиент преждевременно отключился.
            break
        protocol.setChunk(chunk)
    return Protocol.data


async def write_response(writer, response, cid):
    writer(str({"status": "OK"}).encode())
    writer.close()
    print(f'Client #{cid} has been served')


async def run_server(host, port):
    server = await asyncio.start_server(serve_client, host, port)
    await server.serve_forever()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(run_server("localhost", 1234))
    loop.run_forever()
