"""
Template v 0.1
"""
import allure
import pytest
from libs.pages.loginPage import PageLogin
from config import SDO_Accounts

# Test_name

suite_name = "СДО/НСПК"
test_name = "Успеваемость студента"
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
        "remoteIP": "80.87.200.64",
        "remotePort": 4444,
        "executablePath": "./chromedriver"
    }], indirect=True)


@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.flaky(reruns=reruns)
def test_formSending(request, setup_driver, isLastTry, data, reporter):
    page = PageLogin(setup_driver)
    page.getPage("https://sdo.i-college.ru/login/index.php")
    with reporter.allure_step(f"Логинимся как менеджер УЦ", screenshot=True, browserLog=True, alarm=True,
                              ignore=not isLastTry):
        page.login(**SDO_Accounts["SDO"]["nspk"]["study_center_manager"])

    with reporter.allure_step(f"Переход в успеваемость студентов", screenshot=True, browserLog=True, alarm=True,
                              ignore=not isLastTry):
        page.click(xpath='//*[contains(text(),"Успеваемость студентов")]/..')

    with reporter.allure_step(f"Скачиваем индивидуальную ведомость", screenshot=True, browserLog=True, alarm=True,
                              ignore=not isLastTry):
        page.click(xpath='(//*[contains(text(),"Индивидуальная ведомость")])[1]')
        assert page.findDownloadedFile('.xlsx'), "Файл .xlsx с успеваемостью не найден или долго скачивался"
