from io import StringIO

import pytest
import allure
import requests
from xml import etree


def pytest_generate_tests(metafunc):
    if "url" in metafunc.fixturenames:
        # urls = urlsParser(metafunc.config.getoption("site"), metafunc.config.getoption("foo"))
        # metafunc.parametrize("url", urls)
        pass


@pytest.fixture(scope="session")
def Parser():
    return etree.HTMLParser()


@allure.feature("Фильтрация страниц")
@allure.story("Программы")
@allure.severity("Minor")
def test_filterhtml(url, Parser):
    response = requests.get(url)
    html = response.content.decode("utf-8")
    tree = etree.parse(StringIO(html), parser=Parser)
    a_tag = tree.xpath("//a[@href]")
    b_tag = tree.xpath("//b")
    strong_tag = tree.xpath("//strong")
    strong_tag = tree.xpath("//strong")