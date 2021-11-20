import pytest
from time import sleep

#
# @pytest.fixture(scope="session")
# def fixt1(request):
#     with open(request.param, "w") as file:
#         yield file
#
#
from libs.pages.page import Page
from libs.network import Client


def pytest_generate_tests(metafunc):
    metafunc.parametrize("setup_driver_new", [{
        "remoteIP": "80.87.200.64",
        "remotePort": "4444",
        "browser": "Chrome",
    }], indirect=True)
    # metafunc.parametrize("url", ["https://yandex.ru", "https://google.com"])


def test_test(setup_driver_new):
    # from selenium.webdriver import Firefox
    # from selenium import webdriver
    # ff = webdriver.FirefoxOptions()
    # ff.set_capability("version", "93.0")
    # Driver = webdriver.Remote(command_executor='http://80.87.200.64:4444/wd/hub/', options=ff)
    # Driver.get("https://psy.edu.ru/")
    # Driver.save_screenshot("screen.png")
    Driver = setup_driver_new
    client = Client()
    page = Page(webdriver=Driver, alarm=client)
    with page.allure_step('Тест', True, False, False, True):
        page.getPage("https://google.com")
        sleep(1)
        assert False