import re
from selenium.webdriver.common.by import By
from time import sleep
import requests

class WorkDriver:

    driver = None

    def __init__(self, driver):
        self.driver = driver

    def findElement(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

    def findElements(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)

    # data = {"tag": "*", "attrib": {"class": "form", "data-test": ""}}


    # def findElement(self, xpath, element=None):
    #     if type(xpath) == str:
    #         pass
    #     elif type(xpath) == dict:
    #         xpath = DatatoXpath(xpath)
    #     if element:
    #         return element.find_element(By.XPATH, xpath)
    #     else:
    #         return self.driver.find_element(By.XPATH, xpath)
    #
    # def findElements(self, xpath, element=None):
    #     if element:
    #         return element.find_elements(By.XPATH, xpath)
    #     else:
    #         return self.driver.find_elements(By.XPATH, xpath)

    def searchElemAtGranddad(self, granddad, xpath):
        return granddad.find_element(By.XPATH, xpath)

    def searchElemsAtGranddad(self, granddad, xpath):
        return granddad.find_elements(By.XPATH, xpath)

    def searchElemForTagAtGranddad(self, granddad, tag):
        return granddad.find_elements(By.TAG_NAME, tag)
      
    def getAttrForElem(self, elem, attrib):
        # print(attrib)
        return elem.get_attribute(attrib)
        # return elem.get_attribute

    def sleepPage(self, time):
        return sleep(time)

    def addCookie(self, url, cookie_dict):
        if self.driver.get_cookie(name=cookie_dict["name"]) is None:
            # "https://yandex.ru/domain2/domain3"
            # искать третий слэш
            self.driver.get(url=url[0:url.find(".ru") + 3])
            return self.driver.add_cookie(cookie_dict=cookie_dict)

    # def getRequest(self):
    #     return self.driver.requests

    def getAttr(self, elem):
        get_attr = lambda item: self.driver.execute_script('var items = {}; for (index = 0; index < '
                                                      'arguments[0].attributes.length; ++index) { '
                                                      'items[arguments[0].attributes[index].name] = '
                                                      'arguments[0].attributes[index].value }; return '
                                                      'items;', item)
        return get_attr(elem)

    # def getAttr(self, elem):
    #     return self.driver.execute_script('var items = {}; for (index = 0; index < '
    #                                                   'arguments[0].attributes.length; ++index) { '
    #                                                   'items[arguments[0].attributes[index].name] = '
    #                                                   'arguments[0].attributes[index].value }; return '
    #                                                   'items;', elem)

    def getPage(self, url):
        return self.driver.get(url)