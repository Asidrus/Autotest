import json
from time import sleep, time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Page:
    """
    a class for working with elements on a page
    """
    driver = None
    TIMEOUT = 5  # max time of waiting
    STEPTIME = .5  # repetition period

    def __init__(self, webdriver) -> None:
        """Base class for pages

        :param driver: Selenium WebDriver
        """
        self.webdriver = webdriver
        self.driver = webdriver.driver

    def current_url(self):
        return self.driver.current_url

    def attribute(self, elem, attrib):
        return elem.get_attribute(attrib)

    def attributes(self, elem):
        return self.driver.execute_script('var items = {}; for (index = 0; index < '
                                          'arguments[0].attributes.length; ++index) { '
                                          'items[arguments[0].attributes[index].name] = '
                                          'arguments[0].attributes[index].value }; return '
                                          'items;', elem)

    def __data2xpath__(self, data):
        if type(data) == dict:
            tag = data["tag"] if "tag" in data.keys() else "*"
            attrib = {}
            if "attrib" in data.keys():
                attrib = data["attrib"]
            else:
                for key in data.keys():
                    if key != "tag":
                        attrib[key] = data[key]
        elif type(data) == list:
            tag = ""
            attrib = {}
            for item in data:
                for key in item.keys():
                    if key == "tag":
                        tag = item[key]
                    else:
                        attrib[key] = item[key]
            tag = "*" if tag == "" else tag
        elif type(data) == str:
            return data
        else:
            raise TypeError(f"Не могу преобразовать {data=} типа {type(data)} к xpath")
        atts = ''
        for att in attrib:
            atts = atts + f" and @{att}='{attrib[att]}'"
        atts = '[' + atts[5:] + ']'
        return f"//{tag}{atts}"

    def findElement(self, xpath, element=None):
        xpath = self.__data2xpath__(xpath)
        if element:
            return WebDriverWait(self.driver, self.TIMEOUT, self.STEPTIME).until(
                lambda elem: element.find_element(By.XPATH, xpath))
        else:
            return WebDriverWait(self.driver, self.TIMEOUT, self.STEPTIME).until(
                lambda elem: self.driver.find_element(By.XPATH, xpath))

    def findElements(self, xpath, element=None):
        xpath = self.__data2xpath__(xpath)
        if element:
            return WebDriverWait(self.driver, self.TIMEOUT, self.STEPTIME).until(
                lambda elems: element.find_elements(By.XPATH, xpath))
        else:
            return WebDriverWait(self.driver, self.TIMEOUT, self.STEPTIME).until(
                lambda elems: self.driver.find_elements(By.XPATH, xpath))

    def addCookie(self, url, cookie_dict):
        if self.driver.get_cookie(name=cookie_dict["name"]) is None:
            ind = url.find("/", 8)
            if ind > 0:
                self.driver.get(url=url[:ind])
            else:
                self.driver.get(url=url[:])
            return self.driver.add_cookie(cookie_dict=cookie_dict)

    def getPage(self, url, update=True):
        if not update and self.driver.current_url:
            return
        else:
            return self.driver.get(url)

    def sleep(self, time=.05):
        sleep(time)

    def fill(self, text: str, input: object = None, xpath: str = None) -> None:
        """Typing the text into input field

        :@param text: text
        :@param input: input element
        "@param xpath: xpath of element
        """
        if input is None:
            if xpath is not None:
                input = self.findElement(self.__data2xpath__(xpath))
            else:
                raise Exception("Input или xpath не должны быть None")
        try:
            input.clear()
        except:
            Exception(f"Не удалось очистить поле {self.__data2xpath__(self.attributes(input))}, {input}")
        try:
            for symbol in text:
                self.sleep(.05)
                input.send_keys(symbol)
        except:
            Exception(
                f"Не удалось записать текст '{text}' в поле {self.__data2xpath__(self.attributes(input))}, {input}")

    def click(self, elem: object = None, xpath: str = None) -> None:
        if elem is None:
            if xpath is not None:
                elem = self.findElement(self.__data2xpath__(xpath))
            else:
                raise Exception("Elem или xpath не должны быть None")
        self.driver.execute_script(f"window.scrollTo(0, {elem.location['y']-400})")
        start = time()
        while time() - start < self.TIMEOUT:
            try:
                elem.click()
                return True
            except:
                sleep(self.STEPTIME)
        raise TimeoutError(f"Не удалось кликнуть на элемент {self.__data2xpath__(self.attributes(elem))}, {elem}")

    def selectElement(self, elements: list, pattern: dict):
        for arg in elements:
            for key in pattern.keys():
                attr = self.attribute(arg, key)
                if attr is not None:
                    if attr.lower() in pattern[key]:
                        return arg

    def text(self, elem: object = None, xpath: str = None):
        if elem is None:
            if xpath is not None:
                elem = self.findElement(self.__data2xpath__(xpath))
            else:
                raise Exception("Elem или xpath не должны быть None")
        return elem.text

    def findResponse(self, url):
        process_browser_log_entry = lambda entry: json.loads(entry['message'])['message']
        logs = self.driver.get_log('performance')
        events = [process_browser_log_entry(entry) for entry in logs]
        events = [event for event in events if 'Network.response' in event['method']]
        for e in events:
            try:
                if url == e["params"]["response"]["url"]:
                    return e
            except:
                pass