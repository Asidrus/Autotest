from connect.baseApp import WorkDriver
from time import sleep
import pytest

class WorkPage(WorkDriver):

    def writingTextInField(self, xpath, text):
        input = self.findElement(xpath) 
        input.clear()
        input.send_keys(text)
        return input
 
    def clickButton(self, xpath):
        return self.findElement(xpath).click()

    def stopPage(time):
        return sleep(time)


    def addCookie(self, url):
        return self.check_cookie(url, {"name": "metric_off", "value": "1"})

    def sleepPage(time):
        return sleep(time)

    def outTextElem(self, xpath):
        return self.findElement(xpath).text
   
    @pytest.fixture(scope="session")
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
