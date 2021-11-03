from time import sleep
import pytest
from connect.baseApp import WorkDriver


class Pages(WorkDriver):

    def writingTextInField(self, text, input=None, xpath=None):
        if input is None:
            input = self.findElement(xpath=xpath)
        # else:
        #     input = input

        input.clear()
        for symbol in text:
            self.sleepPage(.05)
            input.send_keys(symbol)

    # по аналогии с writingTextInField
    def clickButton(self, xpath: str, granddad=None):
        if granddad is None:
            try:
                button = self.findElement(xpath)
                button.click()
            except:
                return None
        else:
            try:
                button = self.searchElemAtGranddad(granddad, xpath)
                button.click()
            except:
                try:
                    items = self.searchElemAtGranddad(granddad, "input")
                    for item in items:
                        if "отправить" in self.getAttrForElem(item, "value").lower():
                            button = item
                            button.click()
                except:
                    return None

    # def clickButton(self, xpath: str, granddad=None):
    #     try:
    #         button = self.findElement(xpath, granddad)
    #         button.click()
    #     except:
    #         try:
    #             items = self.searchElemAtGranddad(granddad, "input")
    #             for item in items:
    #                 if "отправить" in self.getAttrForElem(item, "value").lower():
    #                     button = item
    #                     button.click()
    #         except:
    #             return None

    def assigningAnArgumentField(self, args, dict):
        for arg in args:
            for key in dict.keys():
                if str.lower(self.getAttrForElem(arg, key)) in dict[key]:
                    return arg

    def sleepPage(self, time):
        return sleep(time)

    def outTextElem(self, xpath):
        return self.findElement(xpath).text

    def clicker(self):
        def _clicker(button):
            for i in range(200):
                try:
                    button.click()
                    return 1
                except:
                    sleep(0.05)
            button.click()

        return _clicker
