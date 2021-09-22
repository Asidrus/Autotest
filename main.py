from config import *
import asyncio
from matplotlib import pyplot as plt
import random
from datetime import datetime, timedelta


async def main(msg):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 1234)
    writer.write(msg.encode())
    writer.close()
    await writer.wait_closed()


def main2():
    timings = []
    for i in range(10):
        timings.append(timedelta(seconds=random.randint(0, i*2)))
    print(timings)
    plt.plot([time.seconds for time in timings])
    plt.savefig("../temp/pic1.png")
    # plt.show()


from datetime import time
if __name__ == "__main__":
    # asyncio.run(main("hi"))
    # main2()
    time(second=1)
    # time.