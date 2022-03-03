"""
Template v 0.1
"""
import json
import allure
import pytest
from libs.pages.loginPage import PageLogin
from config import SDO_Accounts
# Test_name

suite_name = "Мониторинг сайтов"
test_name = "Проверка отправки заявок с ФОС"
severity = "Сritical"

# Rerun config

rerunInfo = {}
reruns = 2


def pytest_generate_tests(metafunc):
    result = [("sdo")]
    metafunc.parametrize("data", result)
    metafunc.parametrize("headers", [{"Test": test_name}])
    metafunc.parametrize("reruns, rerunInfo", [(reruns, rerunInfo)])
    metafunc.parametrize("setup_driver", [{
        # "remoteIP": "80.87.200.64",
        # "remotePort": 4444,
        "executablePath": "./chromedriver"
    }], indirect=True)


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=reruns)
def test_formSending(request, setup_driver, isLastTry, data, reporter):
    isLastTry = False

    page = PageLogin(setup_driver)
    page.getPage("https://sdo.i-college.ru/login/index.php")
    with reporter.allure_step("Логинимся как студент login", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.login(**SDO_Accounts["SDO"]["nspk"]["student"])

    with reporter.allure_step(f"Переход в документы:", screenshot=True, alarm=True, ignore=not isLastTry):

