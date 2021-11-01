from time import sleep
import pytest
from connect.baseApp import WorkDriver


class Pages(WorkDriver):

    def writingTextInField(self, input, text):
        input.clear()
        for symbol in text:
            self.sleepPage(.05)
            input.send_keys(symbol)

    def clickButton(self, granddad, xpath):
        try:
            button = self.searchElemForTagAtGranddad(granddad, xpath)
            button.click()
        except:
            try:
                items =  self.searchElemForTagAtGranddad(granddad, "input")
                for item in items:
                    if "отправить" in self.getAttrForElem(item, "value").lower():
                        item.click()
            except:
                print("кнопка не обнаружена")


    def sleepPage(self, time):
        return sleep(time)

    def outTextElem(self, xpath):
        return self.findElement(xpath).text
    
    def clicker():
        def _clicker(button): 
            for i in range(200):
                try:
                    button.click()
                    return 1
                except:
                    sleep(0.05)
            button.click()
        return _clicker
