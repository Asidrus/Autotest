# /*выборка элементов со страницы*/
from time import sleep
from os import access


class WorkWithDriver:


    def __init__(self, driver):
        self.driver = driver

    def find_element(self, xpath):
        try:
            return self.driver.find_element_by_xpath(xpath)
        except Exception as e:   
            return 'Can`t find element by page'   

    def findElements(self, xpath): 
        try:
            return self.driver.find_elements_by_xpath(xpath)
        except Exception as e:
            return 'Can`t find elements by page'
     
    # def check_cookie(self, url, cookie_dict): <- тоже надо сюда же
    #     if self.driver.get_cookie(name=cookie_dict["name"]) is None:
    #         self.driver.get)(url=url[0:url.find(".ru") + 3]
    #         self.driver.add_cookie)(cookie_dict=cookie_dic


    def sleepPage(self, time):
        sleep(time)

    def getAttribute(self):
        return lambda item: self.driver.execute_script('var items = {}; for (index = 0; index < '
                                                      'arguments[0].attributes.length; ++index) { '
                                                      'items[arguments[0].attributes[index].name] = '
                                                      'arguments[0].attributes[index].value }; return '
                                                      'items;', item)

    def starDriver(self, url):
        return self.driver.get(url)
