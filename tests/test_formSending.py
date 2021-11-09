import json
from io import StringIO
import asyncio
import allure
import os
from datetime import datetime, timedelta
from config import autotest_results
from conftest import allure_step
from libs.aioparser import aioparser
from libs.pages.formPage import PageForm
import aiohttp
from lxml import etree


suite_name = "Проверка отправки заявок с ФОС"
test_name = "Проверка отправки заявок с ФОС"
severity = "Сritical"
__alarm = f"{severity}: {suite_name}: {test_name}:"

ignores = ["blockPopupByTrigger", "formAddReview"]


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
    fname = autotest_results + f"/{domain}_form.json"

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
    for form in Data["data"]:
        if form["data-test"] in ignores:
            Data["data"].remove(form)
    result = [(item["url"], item["data-test"]) for item in Data["data"]]
    metafunc.parametrize("url, datatest", result)
    # parametrize the webdriver
    metafunc.parametrize("setup_driver_new", [{
        "remoteIP": "80.87.200.64",
        "remotePort": 4444
         }], indirect=True)


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
def test_formSending(setup_driver_new, url, datatest):
    page = PageForm(setup_driver_new)
    with allure_step("Добавление cookie"):
        page.addCookie(url, {"name": "metric_off", "value": "1"})
    with allure_step(f"Переход на страницу {url=}", _alarm=__alarm):
        page.getPage(url)
    with allure_step("Инициализация формы"):
        page.findform(xpath={"tag": "form", "data-test": datatest}, _alarm=__alarm)
    with allure_step("Отправка заявки", page.driver, True, True, _alarm=__alarm):
        confirmation = page.Test()
    with allure_step(f"Проверка результата {url=}, {datatest=}", _alarm=__alarm):
        if confirmation:
            assert True
        else:
            assert False, "Не найднено сообщение об успешной отправки"