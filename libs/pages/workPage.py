from time import sleep
from libs.baseApp import WorkDriver

# a class for working with elements on a page

class Pages(WorkDriver):

    def writingTextInField(self, text, input=None, xpath=None):
        if input is None:
            input = self.findElement(xpath=xpath)

        input.clear()
        for symbol in text:
            self.sleepPage(.05)
            input.send_keys(symbol)


    def clickButton(self, xpath: str, granddad=None):
        try:
            button = self.findElement(xpath, granddad)
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

    def assigningAnArgumentField(self, args, dict):
        for arg in args:
            for key in dict.keys():
                if str.lower(self.getAttrForElem(arg, key)) in dict[key]:
                    return arg

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
