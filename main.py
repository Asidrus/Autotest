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
    print(form.Test())
    driver.close()
    driver.quit()


def _test():
    from func4test import _urlsParser, GenData
    data = _urlsParser("https://pentaschool.ru", parse=False)
    urls = [link["url"] for link in data["links"]]
    gendata = GenData(urls)
    # data = [{"url": "", "xpath": ""}, {"url": "", "xpath": ""}]
    data = []
    for item in gendata:
        if data == 0:
            data.append(item)
        else:
            count = 0
            if len([True for dat in data if dat["xpath"]==item["xpath"]])==0:
                data.append(item)
        print(data)
    result = [(item["url"], item["xpath"]) for item in data]
    print(result)


if __name__ == "__main__":
    # main()
    _test()