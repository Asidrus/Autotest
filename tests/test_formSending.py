import json
from io import StringIO
import asyncio
import allure
import os
from datetime import datetime, timedelta
import pytest
from config import autotest_results, TelegramIP, TelegramPORT
from libs.network import Client
from libs.aioparser import aioparser
from libs.pages.formPage import PageForm
import aiohttp
from config import logger
from lxml import etree
from libs.reporter import Reporter

suite_name = "Проверка отправки заявок с ФОС"
test_name = "Проверка отправки заявок с ФОС"
severity = "Сritical"
__alarm = f"{severity}: {suite_name}: {test_name}:"

ignores = ["blockPopupByTrigger", "formAddReview"]

rerunInfo = {}
reruns = 2


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
                forms = tree.xpath("//*[@data-test]")
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
            (datetime.now()-datetime.fromtimestamp(os.path.getmtime(fname))) < timedelta(hours=23)):
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
    metafunc.parametrize("url, data", result)
    metafunc.parametrize("reruns, rerunInfo", [(reruns, rerunInfo)])
    metafunc.parametrize("setup_driver", [{
        "remoteIP": "80.87.200.64",
        "remotePort": 4444,
        "executablePath": "/home/evgenii/autotest/Autotest/chromedriver"
         }], indirect=True)


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=reruns)
def test_formSending(request, setup_driver, url, data, isLastTry):
    datatest = data
    reporter = Reporter(header=__alarm+f"\n{url=}\n{datatest=}",
                        logger=logger,
                        webdriver=setup_driver,
                        telegram=Client(TelegramIP, TelegramPORT),
                        debug=int(request.config.getoption("--fDebug")))
    page = PageForm(setup_driver)
    with reporter.allure_step("Добавление cookie", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.addCookie(url, {"name": "metric_off", "value": "1"})
    with reporter.allure_step(f"Переход на страницу {url=}", screenshot=True, browserLog=True, alarm=True,
                              ignore=not isLastTry):
        page.getPage(url)
    with reporter.allure_step("Инициализация формы", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.findform(xpath={"tag": "*", "data-test": datatest})
    with reporter.allure_step("Отправка заявки", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        confirmation = page.Test()
    with reporter.allure_step(f"Проверка результата", screenshot=True, alarm=True, ignore=not isLastTry):
        assert confirmation, "Не найднено сообщение об успешной отправки"