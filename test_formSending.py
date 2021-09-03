import allure
from allure_commons.types import AttachmentType
import pytest
from time import sleep
from seleniumwire import webdriver
from libs.form import *
from func4test import *
import requests


def pytest_generate_tests(metafunc):
    urls = urlsParser(metafunc.config.getoption("site"), metafunc.config.getoption("parse"))['links']
    with open("forms.json", "r") as read_file:
        Data = json.load(read_file)
        read_file.close()
    data = []
    for item in Data["data"]:
        if data == 0:
            data.append(item)
        else:
            count = 0
            if len([True for dat in data if dat["xpath"] == item["xpath"]]) == 0:
                data.append(item)
    result = [(item["url"], item["xpath"]) for item in data]
    metafunc.parametrize("url, xpath", result)


def step(func):
    def wrapper(*args, _error=None, _screenshot=None, _driver=None, _step=None, **kwargs):
        with allure.step(_step):
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                if _screenshot:
                    allure.attach(_driver.get_screenshot_as_png(), name="Screenshot",
                                  attachment_type=AttachmentType.PNG)
                if _error is None:
                    raise e
                else:
                    raise Exception(_error)

    return wrapper


@step
def check_cookie(driver, url, cookie_dict):
    if driver.get_cookie(name=cookie_dict["name"]) is None:
        step(driver.get)(url=url[0:url.find(".ru") + 3])
        step(driver.add_cookie)(cookie_dict=cookie_dict)


@allure.feature("Тест форм")
@allure.story("Форма")
@allure.severity("Critical")
def test_formSending(setup_driver, url, xpath):
    driver = setup_driver
    check_cookie(driver, url, {"name": "metric_off", "value": "1"}, _step="Добавление cookie")
    step(driver.get)(url, _step=f"Переход на страницу {url=}")
    sleep(2)
    form = step(Form)(xpath=xpath, driver=driver, _step="Инициализация формы")
    if not form.isready:
        pytest.skip(f"Form is not define as FeedBackForm on {url=} with {xpath=}")
    request, confirmation = step(form.Test)(_driver=driver, _screenshot=True, _step="Отправка заявки")
    with allure.step("Анализ результата"):
        if request is None and confirmation:
            with allure.step("Screenshot"):
                allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
            raise Exception(f"Запрос не найден, а подтвреждение да. Требуется перепроверка.")
        if request is None and not confirmation:
            with allure.step("Screenshot"):
                allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
            assert Exception(f"Не найден запрос и подтверждения. Все сломалось.")
        if request is not None:
            status_code = request.response.status_code
            if status_code // 100 == 2:
                if confirmation:
                    assert True, str(request.response.body.decode("UTF-8") + str(request.response))
                else:
                    raise "Status_code 200, а подтверждения нет"
            else:
                if confirmation:
                    raise "Подтверждение есть, а статус код не 200"
                else:
                    with allure.step("Screenshot"):
                        allure.attach(driver.get_screenshot_as_png(), name="Screenshot",
                                      attachment_type=AttachmentType.PNG)
                    assert False, str(request.response.body.decode("UTF-8") + str(request.response))