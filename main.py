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
    options = webdriver.ChromeOptions()
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    # options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = webdriver.Chrome("./resources/chromedriver", options=options)

    try:
        mainUrl = "https://sdo.niidpo.ru/login/index.php"
        time1 = datetime.datetime.now()
        driver.get(mainUrl)
        name = driver.find_element("xpath", "//input[@name='username']")
        password = driver.find_element("xpath", "//input[@name='password']")
        button = driver.find_element("xpath", "//button[@type='submit']")
        name.send_keys(listener_login)
        password.send_keys(listener_password)
        button.click()
        logs = driver.get_log("performance")
        events = [process_browser_log_entry(entry) for entry in logs]
        events = [event for event in events if 'Network.response' in event['method']]
        reqs = []
        for e in events:
            try:
                if "https://sdo.niidpo.ru/" == e["params"]["response"]["url"] or "https://sdo.niidpo.ru/login/index.php" == e["params"]["response"]["url"]:
                    reqs.append(datetime.datetime.fromtimestamp(e["params"]["response"]["responseTime"]/1000))
            except:
                pass
        print(reqs[1]-reqs[0])
        print(datetime.datetime.now()-reqs[1])

        # with open("tmp2.json", "w") as file:
        #     json.dump({"data": reqs}, file, indent=4)

    except Exception as e:
        raise e
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()
