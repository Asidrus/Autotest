import pytest
import os
from time import sleep
from datetime import datetime
from os import sys
from seleniumwire import webdriver
import allure
from allure_commons.types import AttachmentType
from pyvirtualdisplay import Display
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

path = os.path.abspath(os.getcwd())
path_of_driver = path + "/resources/chromedriver" if sys.platform == "linux" else path + "/resources/chromedriver.exe"


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
        Driver = webdriver.Chrome(path_of_driver, desired_capabilities=d, options=chrome_options)
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


def step(func):
    def wrapper(*args, _error=None, _screenshot=None, _driver=None, _step=None, **kwargs):
        with allure.step(_step):
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                if _screenshot:
                    allure.attach(_driver.get_screenshot_as_png(), name="Screenshot",
                                  attachment_type=AttachmentType.PNG)
                if _error is None:
                    raise e
                else:
                    raise Exception(_error)
    return wrapper


@step
def check_cookie(driver, url, cookie_dict):
    if driver.get_cookie(name=cookie_dict["name"]) is None:
        step(driver.get)(url=url[0:url.find(".ru") + 3])
        step(driver.add_cookie)(cookie_dict=cookie_dict)



@pytest.fixture(scope="function")
def timing():
    startTime = datetime.now()

    def deltaTime():
        return datetime.now() - startTime

    return deltaTime


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
