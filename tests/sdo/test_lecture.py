"""
Template v 0.1
"""
import allure
import pytest
from libs.pages.loginPage import PageLogin
from libs.pages.sdo.lecturePage import PageLecture
from config import SDO_Accounts, downloads_path
# Test_name

suite_name = "СДО/ОСЕК"
test_name = "Проверка лекции и скачивания"
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
    page.getPage("https://sdo.i-spo.ru/login/index.php")
    with reporter.allure_step(f"Логинимся как студент", screenshot=True, browserLog=True, alarm=True, ignore=not isLastTry):
        page.login(**SDO_Accounts["SDO"]["osek"]["student2"], checkboxes=['//input[@id="user_approvement"]'])

    page = PageLecture(setup_driver)

    with reporter.allure_step(f"Переход в лекцию", screenshot=True, alarm=True, ignore=not isLastTry):
        page.go2lecture()

    with reporter.allure_step(f"Клик на след. страницу", screenshot=True, alarm=True, ignore=not isLastTry):
        page.nextPage()

    with reporter.allure_step(f"Клик на пред. страницу", screenshot=True, alarm=True, ignore=not isLastTry):
        page.backPage()

    with reporter.allure_step(f"Скачать лекцию", screenshot=True, alarm=True, ignore=not isLastTry):
        page.downloadLecture()
        assert page.findDownloadedFile(), "скачанный файл .pdf с лекцией не найден"

    with reporter.allure_step(f"Развернуть лекцию на весь экран", screenshot=True, alarm=True, ignore=not isLastTry):
        page.backPage()


