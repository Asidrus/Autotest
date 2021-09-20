from config import *
import asyncio


async def main(msg):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 1234)
    writer.write(msg.encode())
    writer.close()
    await writer.wait_closed()




if __name__ == "__main__":
    asyncio.run(main(msg))
