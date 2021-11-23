from config import *
from conftest import db_connection
import allure
import pytest
import asyncio
from libs.network import Client
import requests
from libs.reporter import Reporter

suite_name = "Мониторинг сайтов"
test_name = "Статус ответа"
severity = "Сritical"
__alarm = f"{severity}: {suite_name}: {test_name}: "
db_name = "speedtest"
db_data = {"user": db_login, "password": db_password, "database": db_name, "host": db_host}

codes = {1: True, 2: True, 3: True, 4: False, 5: False}


@db_connection(**db_data)
async def getData(connection):
    urls = await connection.fetch("SELECT url FROM urls;")
    return urls


def pytest_generate_tests(metafunc):
    urls = asyncio.run(getData())
    metafunc.parametrize("url", [url["url"] for url in urls])


rerunInfo = {}
reruns = 2


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=2)
def test_pageStatus(request, url):
    reporter = Reporter(header=__alarm,
                        logger=logger,
                        telegram=Client(TelegramIP, TelegramPORT),
                        debug=int(request.config.getoption("--fDebug")))
    global rerunInfo
    if url in rerunInfo.keys():
        rerunInfo[url] = rerunInfo[url] + 1
    else:
        rerunInfo[url] = 0
    isLastTry = (reruns == rerunInfo[url])
    with reporter.step(f'Connect to {url}', True, not isLastTry):
        response = requests.get(url, timeout=15)
    with reporter.step(f'{url} Check status-code {response.status_code}', True, not isLastTry):
        assert codes[response.status_code // 100]