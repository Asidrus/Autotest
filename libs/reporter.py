import asyncio
from contextlib import contextmanager
from time import time

import allure
from allure_commons.types import AttachmentType

from libs.network import Client
from libs.webdriver import WebDriver


class Reporter:

    header = ''
    logger = None
    webdriver = None
    driver = None
    telegram = None
    debug = None
    screenshot = None

    def __init__(self, header='',
                 logger=None,
                 webdriver: WebDriver = None,
                 telegram: Client = None,
                 debug = 0):
        self.header = header
        self.logger = logger
        self.webdriver = webdriver
        if self.webdriver:
            self.driver = webdriver.driver
        self.telegram = telegram
        self.debug = debug

    def takeScreenshot(self):
        if self.driver:
            self.screenshot = self.driver.get_screenshot_as_png()

    def gatherBrowserLogs(self):
        if self.logger and self.webdriver and self.webdriver.logs:
            self.logger.warning(
                {"url": self.driver.current_url,
                 "messages": self.driver.get_log('browser')})

    def sendToTelegram(self, stepName, error):
        try:
            data = {"content": f"{self.header}\nШаг '{stepName}' провален\nОшибка:\n{str(error)[:30]}",
                    "debug": self.debug,
                    "contentType": 'text'}
            if self.screenshot:
                data['image'] = self.screenshot

            asyncio.run(self.telegram.send(**data))
        except Exception as e:
            if self.logger:
                self.logger.critical(f"Не смог отправить сообщение в ТГ")
            raise e

    @contextmanager
    def step(self, stepName: str,
             screenshot: bool = False,
             browserLog: bool = False,
             alarm: bool = False,
             ignore: bool = False):
        with allure.step(stepName):
            try:
                yield
            except Exception as e:
                self.takeScreenshot()
                if screenshot and self.driver:
                    allure.attach(self.screenshot,
                                  name=stepName,
                                  attachment_type=AttachmentType.PNG)
                if browserLog:
                    self.gatherBrowserLogs()
                if alarm:
                    self.sendToTelegram(stepName, e)
                if self.logger:
                    self.logger.critical(f"{self.header}|{stepName}|" + str(e))
                if ignore is not True:
                    raise Exception(e)
