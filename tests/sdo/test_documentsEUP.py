"""
Template v 0.1
"""
import allure
import pytest
from libs.pages.loginPage import PageLogin
from config import SDO_Accounts

# Test_name

suite_name = "СДО/НСПК"
test_name = "Документы по ИУП"
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

    with reporter.allure_step(f"Переход в документы по ИУП", screenshot=True, browserLog=True, alarm=True,
                              ignore=not isLastTry):
        page.click(xpath='//*[contains(text(),"Документы по ИУП")]/..')

    with reporter.allure_step(f"Скачиваем программу в .doc", screenshot=True, browserLog=True, alarm=True,
                              ignore=not isLastTry):
        page.click(xpath='(//a[@title="Скачать doc"])[1]')
        assert page.findDownloadedFile('.doc'), "Файл .doc с программой не найден или долго скачивался"

    with reporter.allure_step(f"Скачиваем программу в .pdf", screenshot=True, browserLog=True, alarm=True,
                              ignore=not isLastTry):
        page.click(xpath='(//a[@title="Скачать pdf"])[1]')
        assert page.findDownloadedFile('.pdf'), "Файл .pdf с программой не найден или долго скачивался"
