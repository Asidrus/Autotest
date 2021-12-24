import csv
import json

import allure
from allure_commons.types import AttachmentType
import pytest
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from libs.GoogleSheets.GoogleSheets import GoogleSheets
from config import *
from conftest import allure_step
from time import sleep, time
from datetime import datetime

from libs.pages.loginPage import PageLogin

suite_name = "Мониторинг сайтов"
test_name = "Сбор времени от sdo.niidpo.ru"
severity = "Сritical"
__alarm = f"{severity}: {suite_name}: {test_name}: "
times = []

checkStatus = {1: True, 2: True, 3: True, 4: False, 5: False}


@pytest.fixture(scope="session")
def write_log():
    test_datetime = datetime.now()
    yield
    writeIntoFile(test_datetime, times)
    sendInGoogleSheet(test_datetime, times)


def sendInGoogleSheet(test_datetime, times):
    try:
        report = GoogleSheets(SSID=listener_months_SSID[test_datetime.date().month], typeOfDoc="Timings",
                              CREDENTIALS_FILE=google_token)
        m = times.copy()
        m.insert(0, str(test_datetime))
        report.addData(sheet=report.__Sheets__[test_datetime.date().day - 1], data=[m[0:12]])
    except Exception as e:
        logger.critical(str(e))
        raise e


def writeIntoFile(test_datetime, times):
    with open(autotest_results + "/sdo.csv", "a") as f_obj:
        fn = ['Role', 'DateTime']
        for i in range(15):
            fn.append(f"time{i + 1}")
        writer = csv.DictWriter(f_obj, fieldnames=fn, delimiter=',')
        data = {'DateTime': test_datetime}
        for i in range(len(times)):
            data[f"time{i + 1}"] = times[i]
        writer.writerow(data)


def waitResponse(request, timeout=10, delta=0.25):
    start = time()
    while time() - start < timeout:
        try:
            return request["params"]["response"]["status"]
        except:
            sleep(delta)
    raise TimeoutError("Запрос не найден")


def pytest_generate_tests(metafunc):
    metafunc.parametrize("setup_driver_new", [{
        "remoteIP": "80.87.200.64",
        "remotePort": 4444ма н
@allure.feature(suite_name)
@allure.story(test_name)
@allure.severity(severity)
@pytest.mark.timeout(300)
def test_sdo(setup_driver_new, write_log, clicker):
    mainUrl = "https://sdo.niidpo.ru/login/index.php"
    steps = [
        {
            'xpath': "//a[@href='/course/view.php?id=18611&pid=11245' and @class]",
            'back': False
        },
        {
            'xpath': "(((//li[@id='section-1'])[1])//span[@class='instancename'])[1]",
            'back': True
        },
        {
            'xpath': "(((//li[@id='section-1'])[1])//span[@class='instancename'])[2]",
            'back': True
        },
        {
            'xpath': "(((//li[@id='section-1'])[1])//span[@class='instancename'])[4]",
            'back': True
        },
        {
            'xpath': "(((//li[@id='section-1'])[1])//span[@class='instancename'])[13]",
            'back': True
        },
        {
            'xpath': "(((//li[@id='section-4'])[1])//span[@class='instancename'])[1]",
            'back': True
        },
        {
            'xpath': "(//div[@class='sidenav-title'])[2]",
            'back': False
        },
        {
            'xpath': "(//div[@class ='sidenav-title'])[3]",
            'back': False
        },
        {
            'xpath': "(//div[@class='name-webinar'])[9]",
            'back': False
        },
    ]
    reqs = []
    page = PageLogin(setup_driver_new, logger)
    with allure_step(f"Переход на страницу url={mainUrl}", page.driver, True, True,
                     _alarm=__alarm + f"Проблема с загрузкой {mainUrl}"):
        page.getPage(mainUrl)
    reqs.append(page.findResponse("https://sdo.niidpo.ru/login/index.php"))
    if not checkStatus[waitResponse(reqs[0]) // 100]:
        raise Exception(f"Ответ от сервера:{reqs[0]['params']['response']['status']}")
    page.gatherBrowserLogs()
    with allure_step(f"Вход в личный кабинет", page.driver, True, True,
                     _alarm=__alarm):
        page.login(listener_login, listener_password)
        page.gatherBrowserLogs()

    reqs.append(page.findResponse("https://sdo.niidpo.ru/"))
    _ = waitResponse(reqs[1])
    getTime = lambda req: datetime.fromtimestamp(req["params"]["response"]["responseTime"] / 1000)
    times.append(getTime(reqs[1]) - getTime(reqs[0]))
    start_task = datetime.now()
    for step in steps:
        with allure_step("Шаг по клику на" + str(step["xpath"]), page.driver, True, True):
            button = page.findElement(step['xpath'])
            page.gatherBrowserLogs()
            page.click(button)
            times.append(datetime.now() - start_task)
            if step["back"]:
                page.driver.back()
                page.gatherBrowserLogs()
            start_task = datetime.now()
    _ = page.findElement("//p[@onclick='window.history.back()']")
    times.append(datetime.now() - start_task)
    assert True

