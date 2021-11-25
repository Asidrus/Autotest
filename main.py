import asyncio
import logging
from time import sleep

import aiohttp

from libs.network import Client
from libs.pages.testpage import TestPage
from libs.search_content_ import main


import sys

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://pentaschool.ru") as response:
            header = response.headers["Content-Type"]
            print(header[header.find("=")+1:])


if __name__ == "__main__":
    # pattern = ["бессрочн", "библиоклуб", "biblioclub"]
    # pattern = ['образца']
    # main(sys.argv[1], "windows-1251", pattern)
    asyncio.run(main())

