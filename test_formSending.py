import allure
from allure_commons.types import AttachmentType
from libs.form import *
from conftest import *
import os
from datetime import datetime, timedelta
from config import resources_path
from libs.aioparser import aioparser

import aiohttp
from lxml import etree


suite_name = "Проверка отправки заявок с ФОС"
test_name = "Проверка отправки заявок с ФОС"
severity = "Сritical"
__alarm = f"{severity}: {suite_name}: {test_name}:"


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


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
def test_formSending(setup_driver, url, datatest):
    driver = setup_driver
    getAttribute = lambda item: driver.execute_script('var items = {}; for (index = 0; index < '
                                                      'arguments[0].attributes.length; ++index) { '
                                                      'items[arguments[0].attributes[index].name] = '
                                                      'arguments[0].attributes[index].value }; return '
                                                      'items;', item)

    with allure_step("Добавление cookie"):
        check_cookie(driver, url, {"name": "metric_off", "value": "1"})
    with allure_step(f"Переход на страницу {url=}"):
        driver.get(url)
    el = driver.find_element("xpath", f"(//form[@data-test='{datatest}'])[1]")
    xpath = DataToXpath({"tag": "form", "attrib": getAttribute(el)})
    with allure_step("Инициализация формы"):
        form = Form(xpath=xpath, driver=driver)
    if not form.isready:
        raise Exception(f"Невозможно инициализировать форму {form.name=},{form.phone=}")
    with allure_step("Отправка заявки", driver, True, True, _alarm=__alarm):
        # answer, confirmation = form.Test()
        confirmation = form.Test()
    with allure_step(f"Проверка результата {url=}, {datatest=}", _alarm=__alarm):
        if confirmation:
            assert True
        else:
            assert False, "Не найднено сообщение об успешной отправки"

    # if answer and confirmation:
    #     assert True
    # elif not (answer or confirmation):
    #     assert (answer and confirmation), f"Форма не отправлена"
    # elif not answer:
    #     assert False, "Не найдено подтверждение в ответе от сервера"
    # elif not confirmation:
    #     assert False, "Не найднено сообщение об успешной отправки"
