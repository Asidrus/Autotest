from datetime import datetime
import aiohttp
import asyncio
from lxml import etree
from io import StringIO
import requests
from libs.aioparser import aioparser



def _test():
    parser = aioparser()
    parser.getAllUrls(site="https://pentaschool.ru", parse=True)


if __name__ == "__main__":
    start = datetime.now()
    _test()
    print(datetime.now()-start)

