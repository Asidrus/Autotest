from config import *
from conftest import alarm, db_connection
import allure
import pytest
import asyncio
import aiohttp
from datetime import datetime

suite_name = "Мониторинг сайтов"
test_name = "Сбор времени ответа от сайтов"
severity = "Сritical"

codes = {1: True, 2: True, 3: True, 4: False, 5: False}

db_name = "speedtest"
db_data = {"user": db_login, "password": db_password, "database": db_name, "host": db_host}


@db_connection(**db_data)
async def getData(connection):
    urls = await connection.fetch("SELECT * FROM URLS;")
    return urls


def pytest_generate_tests(metafunc):
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
    start_time = datetime.now()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                T = codes[response.status // 100]
                if not T:
                    alarm(f"{severity}: {suite_name}: {test_name}: {url=} имеет статус код [{response.status} {response.reason}]")
                    await db.fetch(f"INSERT INTO TIMINGS (DATETIME, SPEED, ERROR, url_id) VALUES('{str(datetime.now())}','{str(datetime.now() - start_time)}', TRUE, {url_id});")
                else:
                    await db.fetch(
                        f"INSERT INTO TIMINGS (DATETIME, SPEED, ERROR, url_id) VALUES('{str(datetime.now())}','{str(datetime.now() - start_time)}', False, {url_id});")
    except:
        await db.fetch(f"INSERT INTO TIMINGS (DATETIME, SPEED, ERROR, url_id) VALUES('{str(datetime.now())}','{str(datetime.now() - start_time)}', TRUE, {url_id});")