import asyncio
import logging
from contextlib import contextmanager
from time import time

import allure
from allure_commons.types import AttachmentType

from libs.network import Client
from libs.pages.page import Page


class TestPage(Page):

    def __init__(self, webdriver, logger: logging = None, alarm: Client = None) -> None:
        super().__init__(webdriver)
        self.logger = logger
        self.alarm = alarm

    def gatherBrowserLogs(self):
        self.logger.warning({"url": self.current_url(), "messages": self.driver.get_log('browser')})

    @contextmanager
    def allure_step(self, step_name: str,
                    screenshot: bool = False,
                    browserLog: bool = False,
                    ignore: bool = False,
                    alarm: bool = False):
        with allure.step(step_name):
            try:
                yield
            except Exception as e:
                if screenshot:
                    _screenshot_ = self.driver.get_screenshot_as_png()
                    allure.attach(_screenshot_, name=step_name, attachment_type=AttachmentType.PNG)
                if browserLog:
                    self.gatherBrowserLogs()
                if self.logger:
                    self.logger.critical(f"{step_name}|" + str(e))
                if self.alarm and alarm:
                    try:
                        d = {'text': f"\nШаг {step_name} провален\nОшибка\n{str(e)[:50]}",
                             'datetime': time(),
                             'debug': 1}
                        data = {"text": str(d).encode()}
                        if screenshot:
                            data['image'] = _screenshot_
                        asyncio.run(self.alarm.send(**data))
                    except Exception as er:
                        e = f"{e}, {er}"
                if ignore is not True:
                    raise Exception(e)