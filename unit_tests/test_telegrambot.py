import json
import allure
import pytest

from libs.network import Client
from libs.reporter import Reporter
from libs.pages.page import Page
from config import TelegramIP, TelegramPORT, logger

# Test_name

suite_name = "Мониторинг сайтов"
test_name = "Проверка отправки заявок с ФОС"
severity = "Сritical"

# Rerun config

rerunInfo = {}
reruns = 2


def pytest_generate_tests(metafunc):
    result = [(1)]
    metafunc.parametrize("data", result)
    metafunc.parametrize("reruns, rerunInfo", [(reruns, rerunInfo)])
    metafunc.parametrize("setup_driver", [{
        "executablePath": "chromedriver",
        "remoteIP": "80.87.200.64",
        "remotePort": 4444
    }], indirect=True)


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=reruns)
def test_formSending(request, setup_driver, isLastTry, data):
    url = request.config.getoption("--site")
    reporter = Reporter(header={"Test": test_name, "url": url},
                        logger=logger,
                        webdriver=setup_driver,
                        telegram=Client("80.87.200.64", 1234),
                        debug=int(request.config.getoption("--fDebug")))

    page = Page(webdriver=setup_driver)

    with reporter.allure_step("Step 1", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.getPage(url)
    with reporter.allure_step(f"Step 2", screenshot=True, alarm=True, ignore=not isLastTry):
        assert False, "Специально ломаю"
