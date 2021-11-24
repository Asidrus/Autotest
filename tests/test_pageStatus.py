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

rerunInfo = {}
reruns = 2


@db_connection(**db_data)
async def getData(connection):
    urls = await connection.fetch("SELECT url FROM urls;")
    return urls


def pytest_generate_tests(metafunc):
    urls = asyncio.run(getData())
    metafunc.parametrize("data", [url["url"] for url in urls])
    metafunc.parametrize("reruns, rerunInfo", [(reruns, rerunInfo)])


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=reruns)
def test_pageStatus(request, data, isLastTry):
    url = data
    reporter = Reporter(header=__alarm,
                        logger=logger,
                        telegram=Client(TelegramIP, TelegramPORT),
                        debug=int(request.config.getoption("--fDebug")))
    with reporter.step(f'Connect to {url}', alarm=True, ignore=not isLastTry):
        response = requests.get(url, timeout=15)
    with reporter.step(f'{url} Check status-code {response.status_code}', alarm=True, ignore=not isLastTry):
        raise Exception('ломаю')
        assert codes[response.status_code // 100]