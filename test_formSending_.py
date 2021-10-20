import allure
from allure_commons.types import AttachmentType
from libs.form import *
from func4test import *
from conftest import *
import os
from datetime import datetime, timedelta
from config import resources_path
from libs.aioparser import aioparser

import aiohttp
from lxml import etree


async def seekForms(urls):
    parser = etree.HTMLParser()
    data = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as response:
                if "text/html" not in response.headers["Content-Type"]:
                    continue
                html = await response.text("utf-8", errors="ignore")
                tree = etree.parse(StringIO(html), parser=parser)
                forms = tree.xpath("//form[@data-test]")
                for el in forms:
                    datatest = el.attrib["data-test"]
                    if not any([(datatest == d["data-test"]) for d in data]):
                        data.append({"url": url, "data-test": datatest})
    return data


def pytest_generate_tests(metafunc):
    site = metafunc.config.getoption("site")
    domain = site.replace("https://", "").replace(".ru", "")
    fname = resources_path + f"/{domain}_form.json"

    if os.path.exists(fname) and (
            (datetime.fromtimestamp(os.path.getmtime(fname)) - datetime.now()) < timedelta(days=1)):
        with open(fname, "r") as read_file:
            Data = json.load(read_file)
            read_file.close()
    else:
        parser = aioparser()
        parser.getAllUrls(site)
        urls = [link["url"] for link in parser.links]
        Data = {"data": asyncio.run(seekForms(urls))}
        with open(fname, "w") as write_file:
            json.dump(Data, write_file, indent=4)
    result = [(item["url"], item["data-test"]) for item in Data["data"]]
    metafunc.parametrize("url, datatest", result)


def test_form_Sending(setup_driver, url, datatest):
    driver = setup_driver
    getAttribute = lambda item: driver.execute_script('var items = {}; for (index = 0; index < '
                                                      'arguments[0].attributes.length; ++index) { '
                                                      'items[arguments[0].attributes[index].name] = '
                                                      'arguments[0].attributes[index].value }; return '
                                                      'items;', item)

    with allure_step("Добавление cookie"):
        check_cookie(driver, url, {"name": "metric_off", "value": "1"})
    with allure_step(f"Переход на страницу {url=}"):
        if driver.current_url != url:
            driver.get(url)
    sleep(2)
    el = driver.find_element_by_xpath(f"(//form[@data-test='{datatest}'])[1]")
    xpath = DataToXpath({"tag": "form", "attrib": getAttribute(el)})
    with allure_step("Инициализация формы"):
        form = Form(xpath=xpath, driver=driver)
    if not form.isready:
        pytest.skip(f"Form is not define as FeedBackForm on {url=} with {xpath=}")
    with allure_step("Отправка заявки", driver, True, True, _alarm=False):
        result, r1, r2 = form.Test()
    assert result, f"{r1=}, {r2=}"