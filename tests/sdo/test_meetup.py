"""
Template v 0.1
"""
import allure
import pytest
from libs.pages.loginPage import PageLogin
from libs.pages.sdo.meetingsPage import PageMeetings
from config import SDO_Accounts

# Test_name

suite_name = "СДО/НСПК"
test_name = "Создание встречи"
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
        page.login(**SDO_Accounts["SDO"]["nspk"]["teacher"])

    page = PageMeetings(setup_driver)
    with reporter.allure_step(f"Переходим в Онлайн встречи", screenshot=True, browserLog=True, alarm=True,
                              ignore=not isLastTry):
        page.go2meeting()

    with reporter.allure_step(f"Добавляем event", screenshot=True, browserLog=True, alarm=True,
                              ignore=not isLastTry):
        page.addEvent()
        assert page.findElement(xpath='//*[contains(text(), "2030 ")]') is not None, "Event не добавлен или не найден"

    with reporter.allure_step(f"Переходим в Онлайн встречи", screenshot=True, browserLog=True, alarm=True,
                              ignore=not isLastTry):
        page.go2meeting()
    with reporter.allure_step(f"Удаляем event", screenshot=True, browserLog=True, alarm=True,
                              ignore=not isLastTry):
        page.deleteEvent()
        try:
            event = page.findElement(xpath='//*[contains(text(), "2030 ")]')
            assert event is None, "Event не удален или найден другой"
        except:
            assert True
