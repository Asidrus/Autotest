from config import *
from conftest import db_connection
import allure
import pytest
import asyncio

from libs.client import Client
import requests

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
    # if metafunc.config.getoption("site"):
    #     site = metafunc.config.getoption("site")
    #     parser = aioparser()
    #     domain = site.lower().replace("https://", "")
    #     parser.getAllUrls(site, metafunc.config.getoption("parse"))
    #     metafunc.parametrize("url", [link["url"] for link in parser.links])
    # else:


rerunInfo = {}
lastTry = 2


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=2)
def test_pageStatus(url):
    global rerunInfo
    if url in rerunInfo.keys():
        rerunInfo[url] = rerunInfo[url] + 1
    else:
        rerunInfo[url] = 0
    alarm = Client(ip="localhost", port=1234, header=__alarm, debug=1)
    try:
        response = requests.get(url, timeout=15)
    except Exception as e:
        print(e)
        alarm.send(alarm.createMessage(f'Bad connection for {url}'))
        assert False
    if codes[response.status_code // 100]:
        assert True
    else:
        alarm.send(alarm.createMessage(f"Site {url} -> ответ {response.status_code}"))
        assert False