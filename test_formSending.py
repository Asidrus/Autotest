import allure
from allure_commons.types import AttachmentType
from libs.form import *
from func4test import *
from conftest import *
import os
from datetime import datetime, timedelta
from config import resources_path
from libs.aioparser import aioparser


# def pytest_generate_tests(metafunc):
#     site = metafunc.config.getoption("site")
#     domain = site.replace("https://", "").replace(".ru", "")
#     fname = resources_path+f"/{domain}_form.json"
#
#     if os.path.exists(fname) and (
#             (datetime.fromtimestamp(os.path.getmtime(fname)) - datetime.now()) < timedelta(days=1)):
#         with open(fname, "r") as read_file:
#             Data = json.load(read_file)
#             read_file.close()
#     else:
#         parser = aioparser()
#         parser.getAllUrls(site)
#         urls = [link["url"] for link in parser.links]
#         Data = {"data": GenData(urls)}
#         with open(fname, "w") as write_file:
#             json.dump(Data, write_file, indent=4)
#
#     data = []
#     for item in Data["data"]:
#         if data == 0:
#             data.append(item)
#         else:
#             if len([True for dat in data if dat["xpath"] == item["xpath"]]) == 0:
#                 data.append(item)
#     result = [(item["url"], item["xpath"]) for item in data]
#     metafunc.parametrize("url, xpath", result)
#
#
# @allure.feature("Тест форм")
# @allure.story("Форма")
# @allure.severity("Critical")
# def test_formSending(setup_driver, url, xpath):
#     driver = setup_driver
#     with allure_step("Добавление cookie"):
#         check_cookie(driver, url, {"name": "metric_off", "value": "1"}, _step="Добавление cookie")
#     step(driver.get)(url, _step=f"Переход на страницу {url=}")
#     sleep(2)
#     form = step(Form)(xpath=xpath, driver=driver, _step="Инициализация формы")
#     if not form.isready:
#         pytest.skip(f"Form is not define as FeedBackForm on {url=} with {xpath=}")
#     request, confirmation = step(form.Test)(_driver=driver, _screenshot=True, _step="Отправка заявки")
#     with allure.step("Анализ результата"):
#         if request is None and confirmation:
#             with allure.step("Screenshot"):
#                 allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
#             raise Exception(f"Запрос не найден, а подтвреждение да. Требуется перепроверка.")
#         if request is None and not confirmation:
#             with allure.step("Screenshot"):
#                 allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
#             assert Exception(f"Не найден запрос и подтверждения. Все сломалось.")
#         if request is not None:
#             status_code = request.response.status_code
#             if status_code // 100 == 2:
#                 if confirmation:
#                     assert True, str(request.response.body.decode("UTF-8") + str(request.response))
#                 else:
#                     raise "Status_code 200, а подтверждения нет"
#             else:
#                 if confirmation:
#                     raise "Подтверждение есть, а статус код не 200"
#                 else:
#                     with allure.step("Screenshot"):
#                         allure.attach(driver.get_screenshot_as_png(), name="Screenshot",
#                                       attachment_type=AttachmentType.PNG)
#                     assert False, str(request.response.body.decode("UTF-8") + str(request.response))

#url="https://niidpo.ru/seminar/4837", xpath="//form[@id='order_form']"
#url="https://pentaschool.ru/program/program-graficheskij-dizajn-v-reklame-s-nulya", xpath="//div[@class='uniform-block-form__items']"
def test_form_Sending(setup_driver, url="https://psy.edu.ru/program/geshtalt-konsultirovanie-v-psihologicheskoj-praktike", xpath="//div[@class='still-quest_elems']"):
    driver = setup_driver
    with allure_step("Добавление cookie"):
        check_cookie(driver, url, {"name": "metric_off", "value": "1"})
    with allure_step(f"Переход на страницу {url=}"):
        if driver.current_url != url:
            driver.get(url)
    sleep(2)
    with allure_step("Инициализация формы"):
        form = Form(xpath=xpath, driver=driver)
    if not form.isready:
        pytest.skip(f"Form is not define as FeedBackForm on {url=} with {xpath=}")
    with allure_step("Отправка заявки", driver, True, True, _alarm=False):
        request, confirmation = form.Test()

    requests = []
    for req in driver.requests:
        try:
            requests.append({
                "url": req.url,
                "path": req.path,
                "host": req.host,
                "params": req.params,
                "querystring": req.querystring,
                "body": req.body.decode()
            })
        except Exception as e:
            requests.append({"error": str(e)})

    with open("./resources/log3.json", "w") as w:
        json.dump({"requests": requests}, w, indent=4)
