from time import sleep
import allure
from allure_commons.types import AttachmentType
from libs.form import *
from libs.func4test import *
from conftest import *
import os
from datetime import datetime, timedelta
from conf.config import resources_path
from libs.aioparser import aioparser
from libs.form import PageForm
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

    page = PageForm(setup_driver)

    with allure_step("Добавление cookie"):
        page.addCookie(url, {"name": "metric_off", "value": "1"})

    with allure_step(f"Переход на страницу {url=}"):
        page.getPage(url)
        page.sleepPage(2)

    el = page.findElement(f"(//form[@data-test='{datatest}'])[1]")
    xpath = DataToXpath({"tag": "form", "attrib": page.getAttr(el)})

    with allure_step("Инициализация формы"):
        page.findform(xpath=xpath)

    if not page.form.isready:
        raise Exception(f"Невозможно инициализировать форму {page.form.name=},{page.form.phone=}")

    with allure_step("Отправка заявки", page.driver, True, True, _alarm=True):
        answer, confirmation = page.Test()
    if answer and confirmation:
        assert True
    elif not (answer or confirmation):
        assert (answer and confirmation), f"Форма не отправлена"
    elif not answer:
        assert False, "Не найдено подтверждение в ответе от сервера"
    elif not confirmation:
        assert False, "Не найдено сообщение об успешной отправки"
