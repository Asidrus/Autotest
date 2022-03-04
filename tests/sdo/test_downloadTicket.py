"""
Template v 0.1
"""
import allure
import pytest
import os
from libs.pages.loginPage import PageLogin
from libs.pages.sdo.documentsPage import PageDocuments
from config import SDO_Accounts, downloads_path
# Test_name

suite_name = "СДО/ОСЕК"
test_name = "Проверка скачивания квитанции об оплате"
severity = "Сritical"

# Rerun config

rerunInfo = {}
reruns = 0


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
    page.getPage("https://sdo.i-spo.ru/login/index.php")
    with reporter.allure_step("Логинимся как студент login", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.login(**SDO_Accounts["SDO"]["osek"]["student2"], checkboxes=['//input[@id="user_approvement"]'])

    with reporter.allure_step(f"Переход в документы:", screenshot=True, alarm=True, ignore=not isLastTry):
        page.go2documents()

    page = PageDocuments(setup_driver)

    with reporter.allure_step(f"Закрываем поп-ап, если есть", screenshot=True, alarm=True, ignore=not isLastTry):
        page.closePopUp()

    with reporter.allure_step(f"Скачать квитанцию", screenshot=True, alarm=True, ignore=not isLastTry):
        page.downloadTicket()
        page.sleep(10)
        assert os.path.exists(downloads_path+'/kvitanzia.rtf'), "скачанный файл kvitanzia.rtf с квитанцией не найден"


