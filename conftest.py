import asyncio
from contextlib import contextmanager

import asyncpg as asyncpg
import pytest
from time import sleep
from datetime import datetime
from seleniumwire import webdriver
import allure
from allure_commons.types import AttachmentType
from pyvirtualdisplay import Display
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from config import *


def pytest_addoption(parser):
    parser.addoption("--invisible", action='store_true', help="Run on virtual display")
    parser.addoption("--adaptive", action='store_true', help="Run as mobile user agent")
    parser.addoption("--fn", type=str, help="Path of file")
    parser.addoption("--site", type=str, help="Url of site")
    parser.addoption("--parse", action='store_true', help="Parse site on urls")


@pytest.fixture(scope="session")
def setup_driver(request):
    try:
        chrome_options = Options()
        if request.config.getoption("--invisible"):
            display = Display(visible=0, size=(1920, 1080))
            display.start()
        if request.config.getoption("--adaptive"):
            chrome_options.add_argument(
                '--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'browser': 'ALL'}
        chrome_options.add_argument("--window-size=1920,1080")
        Driver = webdriver.Chrome(chromedriver, desired_capabilities=d, options=chrome_options)
    except Exception as e:
        raise e
    yield Driver
    try:
        Driver.close()
        Driver.quit()
        if request.config.getoption("--invisible"):
            display.stop()
    except Exception as e:
        raise e


async def send_telegram_broadcast(msg):
    reader, writer = await asyncio.open_connection(
        'localhost', 1234)
    writer.write((msg + "#END").encode())
    writer.close()
    await writer.wait_closed()


def alarm(msg):
    asyncio.run(send_telegram_broadcast(msg))


def gatherBrowserLogs(driver):
    driver.proxy.storage.clear_requests()
    logger.warning({"url": driver.current_url, "messages": driver.get_log('browser')})


def step(func):
    def wrapper(*args,
                _error=None,
                _driver=None,
                _screenshot=None,
                _step=None,
                _browser_log=None,
                _ignore=None,
                **kwargs):
        with allure.step(_step):
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                if _screenshot and (_driver is not None):
                    allure.attach(_driver.get_screenshot_as_png(), name="Screenshot",
                                  attachment_type=AttachmentType.PNG)
                if _browser_log and (_driver is not None):
                    logger.warning({"url": _driver.current_url, "messages": _driver.get_log('browser')})
                logger.critical(f"{_step}|"+str(e))
                if _error is not None:
                    e = Exception(_error)
                if _ignore is not True:
                    raise Exception(_error)

    return wrapper


@contextmanager
def allure_step(step_name=None,
                driver=None,
                screenshot=None,
                browser_log=None,
                ignore=None,
                _alarm=None):
    with allure.step(step_name):
        try:
            yield
        except Exception as e:
            if screenshot and (driver is not None):
                allure.attach(driver.get_screenshot_as_png(), name=step_name, attachment_type=AttachmentType.PNG)
            if browser_log and (driver is not None):
                logger.warning({"url": driver.current_url, "messages": driver.get_log('browser')})
            logger.critical(f"{step_name}|"+str(e))
            if _alarm is not None:
                alarm(_alarm+f"\nШаг{step_name} провален"+f"\nОшибка {str(e)}")
            if ignore is not True:
                raise Exception(e)


def check_cookie(driver, url, cookie_dict):
    if driver.get_cookie(name=cookie_dict["name"]) is None:
        step(driver.get)(url=url[0:url.find(".ru") + 3])
        step(driver.add_cookie)(cookie_dict=cookie_dict)


@pytest.fixture(scope="session")
def clicker():
    def _clicker(driver, button):
        for i in range(200):
            try:
                button.click()
                return 1
            except:
                sleep(0.05)
        button.click()

    return _clicker


@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def db():
    connection = await asyncpg.connect(user=db_login,
                                       password=db_password,
                                       database="speedtest",
                                       host="localhost")
    yield connection
    await connection.close()
