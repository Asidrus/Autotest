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
test_name = "Проверка отправки заявок с niidpo.ru"
severity = "Сritical"
__alarm = f"{severity}: {suite_name}: {test_name}:"


rerunInfo = {}
reruns = 2


def pytest_generate_tests(metafunc):
    metafunc.parametrize("data", ["popup"])
    metafunc.parametrize("reruns, rerunInfo", [(reruns, rerunInfo)])
    metafunc.parametrize("setup_driver", [{
        "remoteIP": "80.87.200.64",
        "remotePort": 4444
         }], indirect=True)


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=reruns)
def test_askPopup(request, setup_driver, isLastTry):
    button = "//button[@class='header-elem-btn-ask']"
    form = "//form[@id='header_feedback']"
    url = "https://niidpo.ru"

    reporter = Reporter(header=__alarm+f"\n{url=}\n{form=}",
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
        if request.config.getoption("--adaptive"):
            page.click(xpath="//button[@class='btn header-elems_btn header-elems_btn-burg head-btn']")
            page.click(xpath='//button[@class="menu-btn-bord action_go_form"]')
        else:
            page.click(xpath=button)
        page.findform(xpath=form)
    with reporter.allure_step("Отправка заявки", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        confirmation = page.Test()
    with reporter.allure_step(f"Проверка результата", screenshot=True, alarm=True, ignore=not isLastTry):
        assert confirmation, "Не найднено сообщение об успешной отправки"


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=reruns)
def test_orderForm(request, setup_driver, isLastTry):
    # button = "//button[@class='header-elem-btn-ask']"
    form = "//form[@id='order_form']"
    url = "https://niidpo.ru/seminar/4813"

    reporter = Reporter(header=__alarm+f"\n{url=}\n{form=}",
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
        page.findform(xpath=form)
    with reporter.allure_step("Отправка заявки", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        confirmation = page.Test()
    with reporter.allure_step(f"Проверка результата", screenshot=True, alarm=True, ignore=not isLastTry):
        assert confirmation, "Не найднено сообщение об успешной отправки"


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=reruns)
def test_oldForm(request, setup_driver, isLastTry):
    button = "//div[@class='but_request copy_request']"
    form = "//form[@id='form_request']" if request.config.getoption("--adaptive") else "//form[@id='order-form-2']"
    url = "https://niidpo.ru/seminar/9570"

    reporter = Reporter(header=__alarm+f"\n{url=}\n{form=}",
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
        if request.config.getoption("--adaptive"):
            page.click(xpath=button)
        page.findform(xpath=form)
    with reporter.allure_step("Отправка заявки", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        confirmation = page.Test()
    with reporter.allure_step(f"Проверка результата", screenshot=True, alarm=True, ignore=not isLastTry):
        assert confirmation, "Не найднено сообщение об успешной отправки"