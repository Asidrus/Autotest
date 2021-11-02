from config import *
from conftest import alarm, db_connection, allure_step
import allure
import pytest
import asyncio
import aiohttp
from datetime import datetime

codes = {1: True, 2: True, 3: True, 4: False, 5: False}


async def test_getSpeed():
    url = "https://doesnotexist.rus"
    with allure_step(f"Получение данных {url=}", _alarm="ошибка"):
        start_time = datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status_code = response.status
    result = codes[status_code // 100]
    with allure_step(f"Обработка результата {url=}", _alarm="ошибка"):
        if not result:
            assert False, status_code
        else:
            assert True
