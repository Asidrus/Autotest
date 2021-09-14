import allure
from libs.aioparser import aioparser
import pytest
import aiohttp
# import requests

codes = {1: True, 2: True, 3: True, 4: False, 5: False}


def pytest_generate_tests(metafunc):
    parser = aioparser()
    parser.getAllUrls(metafunc.config.getoption("site"), metafunc.config.getoption("parse"))
    metafunc.parametrize("link", parser.links)
    # metafunc.parametrize("link", [{"url":"https://pentaschool.ru", "from": []},
    #                               {"url":"https://psy.edu.ru", "from": []}])


# @allure.feature("Тест ссылок")
# @allure.story("Статус страниц")
# @allure.severity("Critical")
# def test_pageStatus(link, timing):
#     response = requests.get(link["url"])
#     codes = {1: True, 2: True, 3: False, 4: False, 5: False}
#     assert codes[response.status_code // 100], f"{response.status_code}, from={link['from']}"


@allure.feature("Тест ссылок")
@allure.story("Статус страниц")
@allure.severity("Critical")
@pytest.mark.asyncio
async def test_pageStatus(link, timing):
    async with aiohttp.ClientSession() as session:
        async with session.get(link["url"]) as response:
            assert codes[response.status_code // 100], f"{response.status_code}, from={link['from']}"