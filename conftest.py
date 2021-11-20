import asyncio
from contextlib import contextmanager
import asyncpg as asyncpg
import pytest
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import allure
from allure_commons.types import AttachmentType
from pyvirtualdisplay import Display
from config import *
from libs.webdriver import WebDriver


def pytest_addoption(parser):
    parser.addoption("--invisible", action='store_true', help="Run on virtual display")
    parser.addoption("--adaptive", action='store_true', help="Run as mobile user agent")
    parser.addoption("--local", action='store_true', help="Run on local machine")
    parser.addoption("--fn", type=str, help="Path of file")
    parser.addoption("--site", type=str, help="Url of site")
    parser.addoption("--parse", action='store_true', help="Parse site on urls")


@pytest.fixture(scope="session")
def setup_driver_new(request):
    opt = lambda o: request.config.getoption(o)
    Driver = WebDriver(invisible=opt("--invisible"),
                       adaptive=opt("--adaptive"),
                       remote=not opt("--local"),
                       logs=True,
                       **request.param)
    Driver.runDriver()
    yield Driver
    del Driver


# @pytest.fixture(scope="session")
# def setup_driver(request):
#     try:
#         options = webdriver.ChromeOptions()
#         # options.add_argument("no-sandbox")
#         # options.add_argument("--disable-gpu")
#         options.add_argument("--window-size=1920,1080")
#         # options.add_argument("--disable-dev-shm-usage")
#         options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
#         # options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
#         if request.config.getoption("--adaptive"):
#             options.add_argument(
#                 '--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
#         if request.config.getoption("--local"):
#             if request.config.getoption("--invisible"):
#                 display = Display(visible=0, size=(1920, 1080))
#                 display.start()
#             service = Service(chromedriver)
#             Driver = webdriver.Chrome(service=service, options=options)
#         else:
#             Driver = webdriver.Remote(command_executor=f"http://{selenoid_IP}:{selenoid_port}/wd/hub", options=options)
#     except Exception as e:
#         raise e
#     yield Driver
#     try:
#         Driver.close()
#         Driver.quit()
#         if request.config.getoption("--invisible"):
#             display.stop()
#     except Exception as e:
#         raise e


def db_connection(**kwargs):
    """
    @db_connection(user="...", password="...", database="...", host="...")
    getData(connection):
        await = connection.fetch("SELECT * FROM ...")
    """

    def _wrapper(func):
        async def wrapper():
            connection = await asyncpg.connect(**kwargs)
            result = await func(connection)
            await connection.close()
            return result

        return wrapper

    return _wrapper


@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def db(request):
    """
    @pytest.mark.parametrize('db', [{
        "user": "...",
        "password": "...",
        "database": "...",
        "host": "..."
    }], indirect=True)
    """
    connection = await asyncpg.connect(**request.param)
    yield connection
    await connection.close()


@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def async_retry(request):
    from libs.client import Client
    for i in range(3):
        try:
            yield Client()
        except:
            break
    if len(Client.messages) > 0:
        Client.send(Client.messages[-1])


@pytest.fixture(scope="function")
def retry(request):
    from libs.client import Client
    for i in range(3):
        try:
            yield Client()
        except:
            break
    if len(Client.messages) > 0:
        Client.send(Client.messages[-1])

