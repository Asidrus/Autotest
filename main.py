from seleniumwire import webdriver
from libs.form import Form
from time import sleep


def main():
    driver = webdriver.Chrome("./resources/chromedriver")
    driver.get("https://pentaschool.ru/")
    sleep(10)
    driver.add_cookie({"name": "metric_off", "value": "1"})
    url = "https://pentaschool.ru/program/program-graficheskij-dizajn-v-reklame-s-nulya?"
    driver.get(url)
    xpath = "//div[@class='uniform-block-form__items']"
    form = Form(xpath=xpath, driver=driver)
    print(Form.ready)
    print(form._Test())
    driver.close()
    driver.quit()


if __name__=="__main__":
    main()