import logging
from time import sleep

from libs.network import Client
from libs.pages.testpage import TestPage
from libs.search_content_ import main

def mgaps():
    pattern = ["гуманитарн", "гапс", "академ", "мисао", "мипк", "институт"]
    main("https://mgaps.ru", "windows-1251", pattern)


if __name__ == "__main__":
    # fname_appendix = "_adaptive" if False else ""
    # pattern = ["гуманитарн", "гапс", "академ", "мисао", "мипк", "институт"]
    # pattern = ["webp"]
    # main("https://mgaps.ru/", "windows-1251", pattern)
    # main("https://psy.dev-u.ru", "utf-8", pattern)
    from libs.webdriver import WebDriver
    driver = WebDriver(remote=False,
                       remoteIP='80.87.200.64',
                       remotePort=4444,
                       browser='Firefox',
                       executablePath='/home/kali/autotest/geckodriver')
    driver.run()
    client = Client()
    page = TestPage(driver, logger=logging, alarm=client)
    with page.allure_step('тест', True, False, False, alarm=True):
        page.getPage('https://google.com')
        raise Exception('error')
    del driver