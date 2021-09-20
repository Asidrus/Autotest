from config import *

import asyncio
import aiohttp

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_getSpeed(db, url):
    start_time = datetime.now()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                db.fetch(f"INSERT INTO TIMINGS (DATETIME, URL, SPEEDTIME, ERROR)"
                         f"VALUES({datetime.now()},{datetime.now()-start_time},{url}, FALSE);")
    except:
        db.fetch(f"INSERT INTO TIMINGS (DATETIME, URL, SPEEDTIME "
        f"VALUES({datetime.now()},{datetime.now() - start_time},{url}, TRUE);")