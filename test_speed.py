from config import *
from conftest import alarm, db_connection, allure_step
import allure
import pytest
import asyncio
import aiohttp
from datetime import datetime

suite_name = "Мониторинг сайтов"
test_name = "Сбор времени ответа от сайтов"
severity = "Сritical"
__alarm = f"{severity}: {suite_name}: {test_name}:"
db_name = "speedtest"
db_data = {"user": db_login, "password": db_password, "database": db_name, "host": db_host}

codes = {1: True, 2: True, 3: True, 4: False, 5: False}


@db_connection(**db_data)
async def getData(connection):
    urls = await connection.fetch("SELECT * FROM URLS;")
    return urls


def pytest_generate_tests(metafunc):
    with allure_step("Сбор urls из БД"):
        urls = asyncio.run(getData())
        metafunc.parametrize("data", urls)


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.asyncio
@pytest.mark.parametrize('db', [db_data], indirect=True)
async def test_getSpeed(db, data):
    url = data["url"]
    url_id = data["url_id"]
    with allure_step(f"Получение данных {url=}", _alarm=__alarm):
        start_time = datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status_code = response.status
    result = codes[status_code // 100]
    with allure_step(f"Обработка результата {url=}", _alarm=__alarm):
        if not result:
            await db.fetch(f"INSERT INTO TIMINGS (DATETIME, SPEED, ERROR, url_id) VALUES('{str(datetime.now())}','{str(datetime.now() - start_time)}', TRUE, {url_id});")
            assert False, status_code
        else:
            await db.fetch(f"INSERT INTO TIMINGS (DATETIME, SPEED, ERROR, url_id) VALUES('{str(datetime.now())}','{str(datetime.now() - start_time)}', False, {url_id});")
            assert True
