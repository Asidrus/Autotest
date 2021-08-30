import allure
import pytest
from func4test import *
import requests


def pytest_generate_tests(metafunc):
    if "url" in metafunc.fixturenames:
        try:
            urls = urlsParser(metafunc.config.getoption("site"), metafunc.config.getoption("parse"))['urls']
            metafunc.parametrize("url", urls)
        except:
            pass

@allure.feature("Тест ссылок")
@allure.story("Статус страниц")
@allure.severity("Critical")
def test_pageStatus(url):
    response = requests.get(url)
    codes = {1: True, 2: True, 3: False, 4: False, 5: False}
    assert codes[response.status_code // 100], response.status_code
