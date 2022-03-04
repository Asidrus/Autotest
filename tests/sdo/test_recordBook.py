"""
Template v 0.1
"""
import allure
import pytest
from libs.pages.loginPage import PageLogin
from libs.pages.sdo.documentsPage import PageDocuments
from config import SDO_Accounts
# Test_name

suite_name = "СДО/НСПК"
test_name = "Электронная зачетная книжка"
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
    page = PageLogin(setup_driver)
    page.getPage("https://sdo.i-college.ru/login/index.php")
    with reporter.allure_step(f"Логинимся как менеджер УЦ", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.login(**SDO_Accounts["SDO"]["nspk"]["study_center_manager"])

    with reporter.allure_step(f"Переход в электронные зачетные книжки", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.click(xpath='//*[contains(text(),"зачетн")]/..')

    with reporter.allure_step(f"Скачивание зачетки", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.click(xpath='(//td[contains(@class, "lastcol")])[1]//a')
        assert page.findDownloadedFile('.pdf'), "скачанный файл .pdf с зачеткой не найден"
