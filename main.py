from selenium import webdriver
from selenium.webdriver.common.by import By
from libs.form import DataToXpath, Form
from config import listener_login, listener_password
import json


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response


def main():
    driver = webdriver.Chrome("./resources/chromedriver")
    try:
        options = webdriver.ChromeOptions()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        mainUrl = "https://sdo.niidpo.ru/login/index.php"
        driver.get(mainUrl)
        name = driver.find_element("xpath", "//input[@name='username']")
        password = driver.find_element("xpath", "//input[@name='password']")
        button = driver.find_element("xpath", "//button[@type='submit']")
        name.send_keys(listener_login)
        password.send_keys(listener_password)
        button.click()
        logs = driver.get_log('performance')
        print(logs)
        events = [process_browser_log_entry(entry) for entry in logs]
        events = [event for event in events if 'Network.response' in event['method']]
        print(events)

    except Exception as e:
        raise e
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()
