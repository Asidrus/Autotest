from config import *
from conftest import db_connection
import allure
import pytest
import asyncio
import requests
from libs.network import Client
from libs.reporter import Reporter
from libs.pages.page import Page

suite_name = "Мониторинг сайтов"
test_name = "Проверка оплаты"
severity = "Сritical"
__alarm = f"{severity}: {suite_name}: {test_name}: "

codes = {1: True, 2: True, 3: True, 4: False, 5: False}

rerunInfo = {}
reruns = 2

urls = ["https://adpo.edu.ru/payment?data=TS%2FKz88vMzgxMDR8w%2BDw4eDw%2FHzF6uDy5fDo7eB8wOvl6vHl5eLt4HxrYWdhcG9sQG1haWwucnV8ODU2OA%3D%3D"]


def pytest_generate_tests(metafunc):
    metafunc.parametrize("data", urls)
    metafunc.parametrize("reruns, rerunInfo", [(reruns, rerunInfo)])
    metafunc.parametrize("setup_driver", [{
        "remoteIP": "80.87.200.64",
        "remotePort": 4444
    }], indirect=True)


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=reruns)
def test_pageStatus(request, setup_driver, data, isLastTry):
    url = data
    alarm = __alarm+'\nАдаптив:' if request.config.getoption("--adaptive") else __alarm
    alarm += "\n" + url
    reporter = Reporter(header=alarm,
                        logger=logger,
                        webdriver=setup_driver,
                        telegram=Client(TelegramIP, TelegramPORT),
                        debug=int(request.config.getoption("--fDebug")))
    page = Page(setup_driver)
    with reporter.allure_step('Переход на страницу', screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.getPage(url)
    with reporter.allure_step('Поиск H1', screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.findElement('//H1')
    with reporter.allure_step('Поиск form', screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.findElement({'tag': 'form', 'method': 'post', 'id': 'formPayment'})
