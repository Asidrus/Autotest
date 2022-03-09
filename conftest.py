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
from libs.reporter import Reporter
from libs.network import Client


def pytest_addoption(parser):
    parser.addoption("--invisible", action='store_true', help="Run on virtual display")
    parser.addoption("--adaptive", action='store_true', help="Run as mobile user agent")
    parser.addoption("--local", action='store_true', help="Run on local machine")
    parser.addoption("--fn", type=str, help="Path of file")
    parser.addoption("--site", type=str, help="Url of site")
    parser.addoption("--parse", action='store_true', help="Parse site on urls")
    parser.addoption("--fDebug", action='store_true', help="Debug flag")


@pytest.fixture(scope="session")
def setup_driver(request):
    opt = lambda o: request.config.getoption(o)
    Driver = WebDriver(invisible=opt("--invisible"),
                       adaptive=opt("--adaptive"),
                       remote=not opt("--local"),
                       logs=True,
                       **request.param)
    Driver.run()
    yield Driver
    del Driver


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


@pytest.fixture(scope='function')
def isLastTry(reruns, rerunInfo, data):
    if data in rerunInfo.keys():
        rerunInfo[data] = rerunInfo[data] + 1
    else:
        rerunInfo[data] = 0
    return reruns == rerunInfo[data]


@pytest.fixture(scope='function')
def reporter(request, headers, setup_driver):
    reporter = Reporter(header=headers,
                        logger=logger,
                        webdriver=setup_driver,
                        telegram=Client(TelegramIP, TelegramPORT),
                        debug=int(request.config.getoption("--fDebug")))
    yield reporter
    del reporter
