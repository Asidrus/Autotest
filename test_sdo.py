import csv
import os
import allure
from allure_commons.types import AttachmentType
import pytest
import json
from func4test import sendReportOnEmail
from datetime import datetime, timedelta
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from libs.GoogleSheets.GoogleSheets import GoogleSheets
from conftest import path
logs = []
times = []
autotest_results = path+"/../autotest-results"


@pytest.fixture(scope="session")
def login():
    def _login(driver, _login, _password):
        name = driver.find_element_by_xpath("//input[@name='username']")
        password = driver.find_element_by_xpath("//input[@name='password']")
        button = driver.find_element_by_xpath("//button[@type='submit']")
        name.send_keys(_login)
        password.send_keys(_password)
        button.click()
    return _login


@pytest.fixture(scope="session")
def write_log():
    test_datetime = datetime.now()
    yield
    # try:
    report = GoogleSheets(SSID="1u88yKDi46j1AjpSxVr2tp1sdt1oKyCzoLkSXZ99cGh4", typeOfDoc="Timings")
    m = times.copy()
    m.insert(0, str(test_datetime))
    report.addData(sheet=report.__Sheets__[test_datetime.date().day - 1], data=[m[0:12]])
    # except:
    #     pass
    with open(autotest_results+"/sdo.csv", "a") as f_obj:
        fn = ['Role', 'DateTime']
        for i in range(15):
            fn.append(f"time{i+1}")
        writer = csv.DictWriter(f_obj, fieldnames=fn, delimiter=',')
        data = {'Role': 'student', 'DateTime': test_datetime}
        for i in range(len(times)):
            data[f"time{i+1}"] = times[i]
        writer.writerow(data)
    with open(autotest_results+"/sdo.log", "a") as f_obj:
        f_obj.write(str({"DateTime": str(test_datetime), "logs": str(logs)})+"\n")
    with open(autotest_results+"/sdo.json", "r") as f_obj:
        data = json.load(f_obj)
    with open(autotest_results+"/sdo.json", 'w') as f_obj:
        data[str(test_datetime)] = logs
        json.dump(data, f_obj, indent=4)


@pytest.fixture(scope="session")
def gather_log():
    def _add_log(driver):
        try:
            logs.append({"url": driver.current_url, "messages": driver.get_log('browser')})
        except:
            pass

    def _crush_log(driver, e):
        logs.append({"url": driver.current_url, "messages": str(e)})
        _add_log(driver)
        # try:
        #     sendReportOnEmail("it@gaps.edu.ru", "Autotest SDO", str(times) + str(logs))
        # except:
        #     pass

    return _add_log, _crush_log


@allure.feature("Тест sdo")
@allure.story("Log in")
@allure.severity("Critical")
@pytest.mark.timeout(300)
@pytest.mark.parametrize("dt", [str(datetime.now())])
def test_login(setup_driver, login, timing, write_log, gather_log, clicker, dt):
    add_log, crush_log = gather_log
    driver = setup_driver
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
            'xpath': "(//div[@class='name-webinar'])[7]",
            'back': False
        },
    ]

    try:
        driver.get(mainUrl)
        logs.append({"url": driver.current_url, "messages": driver.get_log('browser')})
    except Exception as e:
        crush_log(driver, f"Test broken. Can't get page: {mainUrl}")
        assert False, str(e)
    try:
        login(driver, "an.karenovna@yandex.ru", "an.karenovna")
        add_log(driver)
    except Exception as e:
        crush_log(driver, f"Test broken. Can't get page: {mainUrl}")
        assert False, str(e)
    reqs = []
    for request in driver.requests:
        try:
            if "https://sdo.niidpo.ru/login/" in request.url:
                reqs.append(request)
        except:
            pass
    try:
        times.append(reqs[1].date - reqs[0].date)
    except Exception as e:
        logs.append({"url": driver.current_url, "messages": f"Time 1 is not define, cause: {e}"})
        times.append(None)
    try:
        times.append(reqs[2].date - reqs[1].date)
    except:
        logs.append({"url": driver.current_url, "messages": f"Time 2 is not define, cause: {e}"})
        times.append(None)
    try:
        start_task = reqs[2].date
    except:
        start_task = datetime.now()
    try:
        for step in steps:
            button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, step['xpath'])))
            add_log(driver)
            clicker(driver, button)
            times.append(datetime.now()-start_task)
            if step["back"]:
                driver.back()
            start_task = datetime.now()
        EC.element_to_be_clickable((By.XPATH, "//div[@class]"))
        times.append(datetime.now() - start_task)
    except Exception as e:
        with allure.step("Screenshot"):
            allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
        crush_log(driver, e)
        assert False, str(e)
    assert True
