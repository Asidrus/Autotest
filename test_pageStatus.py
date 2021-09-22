import allure
from libs.aioparser import aioparser
import pytest
import aiohttp
# import requests

test_name = "Статус код всех ссылок"
domain = ""
severity = "Blocker"

codes = {1: True, 2: True, 3: True, 4: False, 5: False}


def pytest_generate_tests(metafunc):
    parser = aioparser()
    domain = metafunc.config.getoption("site").lower().replace("https://", "")
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


@allure.feature(domain)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.asyncio
async def test_pageStatus(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link["url"]) as response:
            assert codes[response.status // 100], f"{response.status}, from={link['from']}"