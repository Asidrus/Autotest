import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from libs.form import DataToXpath, Form
from config import listener_login, listener_password
import json


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
        driver.quit()
        # driver.close()



if __name__ == "__main__":
    main()
