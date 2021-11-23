import sys
sys.path.append('/home/kali/autotest')
from libs.webdriver import WebDriver
from libs.pages.page import Page
from time import sleep

webdriver = WebDriver(remote=False)
webdriver.run()
page = Page(webdriver=webdriver)

# page.getPage('https://pentaschool.ru/')
# input = page.findElement('//input[@class="els-form field_are_questions" and @name="phone"]')

page.getPage('https://edu.i-spo.ru/')
input = page.findElement('//input[@id="tel-c" and @type="tel" and @name="phone"]')


page.fill('81234567890', input)

value = page.attribute(input, 'value')

print(value)