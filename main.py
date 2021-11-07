import asyncio
import datetime
import time

import aiohttp
import asyncpg
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from tests.conftest import check_cookie, alarm
from libs.form import DataToXpath, Form
from config import listener_login, listener_password
import json
from libs.form import Form


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response


def main():
    for i in range(30):
        options = webdriver.ChromeOptions()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        # options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        driver = webdriver.Chrome("./resources/chromedriver", options=options)
        driver.get("https://psy.edu.ru")
        driver.add_cookie(cookie_dict={"name": "task_PSY_43", "value": "test"})
        driver.add_cookie(cookie_dict={"name": "psycho_site", "value": "test"})
        driver.add_cookie(cookie_dict={"name": "psycho_site_dev", "value": "test"})
        driver.get("https://psy.edu.ru/blog/chego-boyatsya-psihologi-3-istorii-o-slozhnyh-sessiyah")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'popmechanic-snippet')))
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        form = Form(xpath="//form[@id='form_question']", driver=driver)
        form.Test()
        driver.quit()
        # driver.close()


def main2():
    import csv
    with open('/home/kali/Downloads/data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


codes = {1: True, 2: True, 3: True, 4: False, 5: False}


async def getUrl():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pentaschool.ru") as response:
                status_code = response.status
    except:
        print("error")
    result = codes[status_code // 100]
    if not result:
        print("False")
    else:
        print("True")


from libs.search_content_ import *


def mgaps():
    pattern = ["гуманитарн", "гапс", "академ", "мисао", "мипк", "институт"]
    main("https://mgaps.ru", "windows-1251", pattern)


from config import db_host, db_login, db_password

db_name = "speedtest"


async def db():
    db_data = {"user": db_login, "password": db_password, "database": db_name, "host": db_host}
    connection = await asyncpg.connect(**db_data)
    urls = await connection.fetch("SELECT url FROM urls;")
    connection.close()
    return urls


def formSending():
    url = 'https://pentaschool.ru/program/program-graficheskij-dizajn-v-reklame-s-nulya'
    datatest = 'blockPopupByTrigger'
    driver = webdriver.Chrome("./resources/chromedriver")
    getAttribute = lambda item: driver.execute_script('var items = {}; for (index = 0; index < '
                                                      'arguments[0].attributes.length; ++index) { '
                                                      'items[arguments[0].attributes[index].name] = '
                                                      'arguments[0].attributes[index].value }; return '
                                                      'items;', item)
    check_cookie(driver, url, {"name": "metric_off", "value": "1"})
    driver.get(url)
    el = driver.find_element("xpath", f"(//form[@data-test='{datatest}'])[1]")
    xpath = DataToXpath({"tag": "form", "attrib": getAttribute(el)})
    form = Form(xpath=xpath, driver=driver)
    _alarm = "error"
    step_name = "заполнение формы"
    ignore = None
    try:
        confirmation = form.Test()
    except Exception as e:
        if _alarm is not None:
            try:
                mes = _alarm + f"\nШаг {step_name} провален" + f"\nОшибка {str(e)}"
                print(mes)
                alarm(mes)
            except Exception as er:
                e = f"{e}, {str(er)}"
        if ignore is not True:
            pass
            raise Exception(e)
    # print(confirmation)



if __name__ == "__main__":
    # asyncio.run(getUrl())
    # mgaps()
    # urls = asyncio.run(db())
    # print(urls)
    # formSending()
    import requests
    from libs.pages.workPage import Page
    from libs.baseApp import WorkDriver
    wd = WorkDriver

    p = Page()
    p.fill()
    pass
