import sys

sys.path.insert(0, '/home/kali/autotest/')
from libs.pages.formPage import PageForm
from libs.webdriver import WebDriver


webdriver = WebDriver(executablePath="/home/kali/autotest/chromedriver",
                      remote=False,
                      browser='Chrome')
webdriver.run()
print(webdriver.driver)
url = "https://edu.i-spo.ru"
page = PageForm(webdriver)
page.addCookie(url, {"name": "metric_off", "value": "1"})
page.getPage(url)
page.findform(xpath={"tag": "*", "data-test": "pop_form"})
confirmation = page.Test()
