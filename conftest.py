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
                       local=opt("--local"),
                       logs=True,
                       **request.param)
    Driver.runDriver()
    yield Driver
    del Driver


@pytest.fixture(scope="session")
def setup_driver(request):
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("no-sandbox")
        # options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        # options.add_argument("--disable-dev-shm-usage")
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        # options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        if request.config.getoption("--adaptive"):
            options.add_argument(
                '--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
        if request.config.getoption("--local"):
            if request.config.getoption("--invisible"):
                display = Display(visible=0, size=(1920, 1080))
                display.start()
            service = Service(chromedriver)
            Driver = webdriver.Chrome(service=service, options=options)
        else:
            Driver = webdriver.Remote(command_executor=f"http://{selenoid_IP}:{selenoid_port}/wd/hub", options=options)
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
    logger.warning({"url": driver.current_url, "messages": driver.get_log('browser')})


# def step(func):
#     def wrapper(*args,
#                 _error=None,
#                 _driver=None,
#                 _screenshot=None,
#                 _step=None,
#                 _browser_log=None,
#                 _ignore=None,
#                 **kwargs):
#         with allure.step(_step):
#             try:
#                 res = func(*args, **kwargs)
#                 return res
#             except Exception as e:
#                 if _screenshot and (_driver is not None):
#                     allure.attach(_driver.get_screenshot_as_png(), name="Screenshot",
#                                   attachment_type=AttachmentType.PNG)
#                 if _browser_log and (_driver is not None):
#                     logger.warning({"url": _driver.current_url, "messages": _driver.get_log('browser')})
#                 logger.critical(f"{_step}|" + str(e))
#                 if _error is not None:
#                     e = Exception(_error)
#                 if _ignore is not True:
#                     raise Exception(_error)
#
#     return wrapper


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
            logger.critical(f"{step_name}|" + str(e))
            if _alarm is not None:
                try:
                    alarm(_alarm + f"\nШаг {step_name} провален" + f"\nОшибка {str(e)}")
                except Exception as er:
                    e = f"{e}, {str(er)}"
            if ignore is not True:
                raise Exception(e)


def check_cookie(driver, url, cookie_dict):
    if driver.get_cookie(name=cookie_dict["name"]) is None:
        driver.get(url=url[0:url.find(".ru") + 3])
        driver.add_cookie(cookie_dict=cookie_dict)


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
