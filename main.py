from datetime import datetime
import aiohttp
import asyncio
from lxml import etree
from io import StringIO
import requests

mass = ["https://yandex.ru","https://google.com"]


def func1():
    yield from mass

async def func2():
    async with aiohttp.ClientSession() as session:
        for url in func1():
            async with session.get(url) as response:
                text = await response.text()
                print(text)
                if len(mass)<4:
                    mass.append("https://pentaschool.ru")

def _test():
    loop = asyncio.get_event_loop()
    loop.create_task(func2())
    loop.run_forever()

if __name__ == "__main__":
    # start = datetime.now()
    # from libs.aioparser import aioparser
    # parser = aioparser()
    # loop = asyncio.get_event_loop()
    # # loop.run_until_complete(urlsParser_async("https://pentaschool.ru"))
    # loop.run_until_complete(parser.parse("https://pentaschool.ru"))
    # # urlsParser("https://pentaschool.ru")
    # print(datetime.now()-start)
    _test()
