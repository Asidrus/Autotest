import allure
from allure_commons.types import AttachmentType
import pytest
from time import sleep
from seleniumwire import webdriver
from libs.form import *
from func4test import *

# urls = [
#     "http://46.183.163.61/seminar/ehkonomika-i-upravlenie-na-predpriyatii",
#     "http://46.183.163.61/seminar/hr-menedzhment-operacionnoe-upravlenie-personalom-organizacii",
#     "http://46.183.163.61/seminar/gid-ekskursovod",
#     "http://46.183.163.61/seminar/rukovoditel-administrativno-hozyajstvennogo-otdela-v-organizacii",
#     "http://46.183.163.61/seminar/1"
# ]
# urls = ["https://46.183.163.61/seminar/ehkonomika-i-upravlenie-na-predpriyatii"]


def pytest_generate_tests(metafunc):
    if "url" in metafunc.fixturenames:
        urls = urlsParser(metafunc.config.getoption("site"), metafunc.config.getoption("foo"))
        metafunc.parametrize("url", urls)


@allure.feature("Тест форм")
@allure.story("Форма")
@allure.severity("Critical")
def test_formSending(setup_driver, data):
    url = data["url"]
    xpath = data["xpath"]
    Driver = setup_driver
    Driver.get(url)
    sleep(2)
    form = Form(xpath=xpath, driver=Driver)
    text_before = Driver.find_element_by_xpath("//body").text
    Driver.proxy.storage.clear_requests()
    status = form.Test()
    if status["code"] // 100 == 1:
        pytest.skip(status["message"])
    elif status["code"] // 100 == 2:
        assert True, status
    elif status["code"] // 100 == 4:
        raise Exception(f"{status['code']},{status['message']}")
    elif status["code"] // 100 == 5:
        if status["code"] == 580:
            text_after = Driver.find_element_by_xpath("//body").text
            txt_before, txt_after = compareLists(str2list(text_before), str2list(text_after))
            confirm = ["спасибо", "ваша заявка", "ожидайте", "менеджер"]
            confirmation = any([conf in txt.lower() for txt in txt_after for conf in confirm])
            if confirmation:
                raise Exception(f"Запрос не найден, а подтвреждение да. Требуется перепроверка.")
            else:
                status = form.status(599)
        with allure.step("Screenshot"):
            allure.attach(Driver.get_screenshot_as_png(), name="Screenshot",
                          attachment_type=AttachmentType.PNG)
        assert False, status



# @allure.feature("Тест форм")
# @allure.story("Форма")
# @allure.severity("Critical")
# @pytest.mark.parametrize("url, xpath", GenData(urls))
# def test_formSending(setup_driver, url, xpath):
#     Driver = setup_driver
#     Driver.get(url)
#     sleep(2)
#     form = Form(xpath=xpath, driver=Driver)
#     text_before = Driver.find_element_by_xpath("//body").text
#     Driver.proxy.storage.clear_requests()
#     status = form.Test()
#     if status["code"] // 100 == 1:
#         pytest.skip(status["message"])
#     elif status["code"] // 100 == 2:
#         assert True, status
#     elif status["code"] // 100 == 4:
#         raise Exception(f"{status['code']},{status['message']}")
#     elif status["code"] // 100 == 5:
#         if status["code"] == 580:
#             text_after = Driver.find_element_by_xpath("//body").text
#             txt_before, txt_after = compareLists(str2list(text_before), str2list(text_after))
#             confirm = ["спасибо", "ваша заявка", "ожидайте", "менеджер"]
#             confirmation = any([conf in txt.lower() for txt in txt_after for conf in confirm])
#             if confirmation:
#                 raise Exception(f"Запрос не найден, а подтвреждение да. Требуется перепроверка.")
#             else:
#                 status = form.status(599)
#         with allure.step("Screenshot"):
#             allure.attach(Driver.get_screenshot_as_png(), name="Screenshot",
#                           attachment_type=AttachmentType.PNG)
#         assert False, status
