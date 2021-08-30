import pytest
import os
from time import sleep
from datetime import datetime
from os import sys
from seleniumwire import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

path = os.path.abspath(os.getcwd())
path_of_driver = path + "/resources/chromedriver" if sys.platform == "linux" else path + "/resources/chromedriver.exe"


def pytest_addoption(parser):
    parser.addoption("--invisible", action='store_true', help="Run on virtual display")
    parser.addoption("--fn", type=str, help="Path of file")
    parser.addoption("--site", type=str, help="Url of site")
    parser.addoption("--parse", action='store_true', help="Parse site on urls")


@pytest.fixture(scope="session")
def setup_driver(request):
    try:
        if request.config.getoption("--invisible"):
            display = Display(visible=0, size=(1920, 1080))
            display.start()
        # if request.config.getoption("--adaptive"):
        #     run with mobile user agent
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'browser': 'ALL'}
        chrome_options = Options()
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
