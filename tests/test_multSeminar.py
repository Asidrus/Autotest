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
test_name = "Универсальная защита"
severity = "Сritical"
__alarm = f"{severity}: {suite_name}: {test_name}: "

codes = {1: True, 2: True, 3: True, 4: False, 5: False}

rerunInfo = {}
reruns = 2

urls = ["https://niidpo.ru/seminar/4813",
        "https://niidpo.ru/seminar/7023",
        "https://niidpo.ru/anons/9193",
        "https://urgaps.ru/seminar/280",
        "https://urgaps.ru/seminar/1676",
        "https://urgaps.ru/anons/8919",
        "https://adpo.edu.ru/seminar/5146",
        "https://adpo.edu.ru/anons/8920",
        "https://vgaps.ru/seminar/43",
        "https://vgaps.ru/anons/8670",
        ]


def pytest_generate_tests(metafunc):
    metafunc.parametrize("data", urls)
    metafunc.parametrize("reruns, rerunInfo", [(reruns, rerunInfo)])
    metafunc.parametrize("setup_driver", [{
        "remoteIP": "80.87.200.64",
        "remotePort": 4444,
        "executablePath": './chromedriver'
    }], indirect=True)


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=reruns)
def test_pageStatus(request, setup_driver, data, isLastTry):
    url = data
    reporter = Reporter(header={"Test": test_name, "url": url, "Adaptive": request.config.getoption("--adaptive")},                        logger=logger,
                        webdriver=setup_driver,
                        telegram=Client(TelegramIP, TelegramPORT),
                        debug=int(request.config.getoption("--fDebug")))
    page = Page(setup_driver)
    with reporter.allure_step('Переход на страницу', screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.getPage(url)
    with reporter.allure_step('Поиск H1', screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.findElement('//h1')
    with reporter.allure_step('Поиск form', screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.findElement('//h2')
