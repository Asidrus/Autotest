import datetime
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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


if __name__ == "__main__":
    main2()
