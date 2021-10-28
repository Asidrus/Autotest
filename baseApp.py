

class WorkDriver:

    def __init__(self, driver):
        self.driver = driver

    def findElement(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def findElements(self, xpath):
        return self.driver.find_elements0_by_xpath(xpath)

    def check_cookie(self, url, cookie_dict):
        if self.driver.get_cookie(name=cookie_dict["name"]) is None:
            self.driver.get(url=url[0:url.find(".ru") + 3])
            return self.driver.add_cookie(cookie_dict=cookie_dict)

    def pageCheck(self,  url):
        if self.driver.current_url != url:
            return True
        else:
            return False
            
    def getDriver(self):
        return self.driver

    def getAttrElem(self, elem):
        getAttribute = lambda item: self.driver.execute_script('var items = {}; for (index = 0; index < '
                                                      'arguments[0].attributes.length; ++index) { '
                                                      'items[arguments[0].attributes[index].name] = '
                                                      'arguments[0].attributes[index].value }; return '
                                                      'items;', item)
        return getAttribute(elem)

    def startDriver(self, url):
        return self.driver.get(url)