import csv
import allure
from allure_commons.types import AttachmentType
import pytest
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from libs.GoogleSheets.GoogleSheets import GoogleSheets
from config import *
from conftest import step
from time import sleep

times = []


@pytest.fixture(scope="session")
def write_log():
    test_datetime = datetime.now()
    yield
    try:
        months = {
            8: "1u88yKDi46j1AjpSxVr2tp1sdt1oKyCzoLkSXZ99cGh4",
            9: "1zXsJTkKzEnli-TAIuKL27cV1_54y4BjwOYCNKKYCrSM"
        }
        report = GoogleSheets(SSID=months[test_datetime.date().month], typeOfDoc="Timings",
                              CREDENTIALS_FILE=google_token)
        m = times.copy()
        m.insert(0, str(test_datetime))
        report.addData(sheet=report.__Sheets__[test_datetime.date().day - 1], data=[m[0:12]])
    except Exception as e:
        print(e)
    with open(autotest_results + "/sdo.csv", "a") as f_obj:
        fn = ['Role', 'DateTime']
        for i in range(15):
            fn.append(f"time{i + 1}")
        writer = csv.DictWriter(f_obj, fieldnames=fn, delimiter=',')
        data = {'Role': 'student', 'DateTime': test_datetime}
        for i in range(len(times)):
            data[f"time{i + 1}"] = times[i]
        writer.writerow(data)


def login(driver, _login, _password):
    name = driver.find_element_by_xpath("//input[@name='username']")
    password = driver.find_element_by_xpath("//input[@name='password']")
    button = driver.find_element_by_xpath("//button[@type='submit']")
    name.send_keys(_login)
    password.send_keys(_password)
    button.click()


def do_step(step, driver, start_task):
    button = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, step['xpath'])))
    logger.warning({"url": driver.current_url, "messages": driver.get_log('browser')})
    for i in range(400):
        try:
            button.click()
            break
        except:
            sleep(0.05)
    times.append(datetime.now() - start_task)
    if step["back"]:
        driver.back()
    return datetime.now()


@allure.feature("Тест sdo")
@allure.story("Log in")
@allure.severity("Critical")
@pytest.mark.timeout(300)
@pytest.mark.parametrize("dt", [str(datetime.now())])
def test_login(setup_driver, timing, write_log, clicker, dt):
    gather = lambda: logger.warning({"url": driver.current_url, "messages": driver.get_log('browser')})
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

    step(driver.get)(mainUrl, _step=f"Переход на страницу url={mainUrl}",
                     _driver=driver, _screenshot=True, _browser_log=True)
    gather()
    step(login)(driver, "an.karenovna@yandex.ru", "an.karenovna",
                _step=f"Вход в личный кабинет",
                _driver=driver, _screenshot=True, _browser_log=True)
    reqs = []
    for request in driver.requests:
        try:
            if "https://sdo.niidpo.ru/login/" in request.url:
                reqs.append(request)
        except:
            pass
    step(times.append)(reqs[1].date - reqs[0].date, _error=f"Time 1 is not define, cause", _ignore=True)
    step(times.append)(reqs[1].date - reqs[0].date, _error=f"Time 2 is not define, cause", _ignore=True)
    try:
        start_task = reqs[2].date
    except:
        start_task = datetime.now()

    for part in steps:
        start_task = step(do_step)(part, driver, start_task,
                                   _driver=driver, _screenshot=True,
                                   _step="Шаг по клику на" + str(part["xpath"]),
                                   _browser_log=True)
    WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='attention-aggree']")))
    times.append(datetime.now() - start_task)
    assert True
