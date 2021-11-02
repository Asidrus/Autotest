from config import *
from conftest import alarm, db_connection, allure_step, send_telegram_broadcast
import allure
import pytest
import asyncio
import aiohttp
from libs.aioparser import aioparser
from aiohttp.client_exceptions import ClientConnectionError

suite_name = "Мониторинг сайтов"
test_name = "Статус ответа"
severity = "Сritical"
__alarm = f"{severity}: {suite_name}: {test_name}:"
db_name = "speedtest"
db_data = {"user": db_login, "password": db_password, "database": db_name, "host": db_host}

codes = {1: True, 2: True, 3: True, 4: False, 5: False}


@db_connection(**db_data)
async def getData(connection):
    urls = await connection.fetch("SELECT url FROM urls;")
    return urls


def pytest_generate_tests(metafunc):
    if metafunc.config.getoption("site"):
        site = metafunc.config.getoption("site")
        parser = aioparser()
        domain = site.lower().replace("https://", "")
        parser.getAllUrls(site, metafunc.config.getoption("parse"))
        metafunc.parametrize("url", [link["url"] for link in parser.links])
    else:
        urls = asyncio.run(getData())
        metafunc.parametrize("url", [url["url"] for url in urls])


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.asyncio
async def test_pageStatus(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status_code = response.status
    except ClientConnectionError:
        await send_telegram_broadcast(f"{__alarm} Страница {url=} не отвечает")
    except Exception as e:
        await send_telegram_broadcast(f"{__alarm} Страница {url=} не отвечает. ERROR: {e}")
    result = codes[status_code // 100]
    if not result:
        await send_telegram_broadcast(f"{__alarm} Ответ от {url=} - {status_code}")
        assert False, status_code
    else:
        assert True