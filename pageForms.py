from BaseApp import WorkDriver
from time import sleep
import pytest

class WorkPage(WorkDriver):

    def writingTextInField(self, xpath, text):
        input = self.findElement(xpath) 
        input.send_keys(text)
        return input
              
        
        # что то надо придумать с xpath
 
    def clickButton(self):
        return self.findElement().click()

    def stopPage(time):
        return sleep(time)

    def addCookie(self, url):
        return self.check_cookie(url, {"name": "metric_off", "value": "1"})

    def sleepPage(time):
        return sleep(time)
   
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
