from time import sleep
from func4test import *
import re
import zlib
from urllib.parse import unquote


class Form:
    """
    Class for testing feedback forms
    """
    # HTML objects
    granddad = None
    name = None
    phone = None
    email = None
    button = None
    callButton = None
    # If form if ready for test
    isready = True

    def __init__(self, *args, xpath=None, driver=None, **kwargs):
        """

        :param args: list of input tags if xpath == None
        :param xpath: xpath of form is included all input and button tags
        :param kwargs: driver -> selenium.webdriver
        """
        self.__emailDefault__ = "tester_form@gaps.edu.ru"
        self.__phoneDefault__ = "71234567890"
        self.__nameDefault__ = "Автотест"
        self._email_ = {"class": ["email", "e-mail"], "placeholder": ["email", "e-mail", "email*", "e-mail*"],
                        "name": ["email", "e-mail"]}
        self._phone_ = {"class": ["phone"], "placeholder": ["телефон", "телефон*"], "name": ["phone"]}
        self._name_ = {"class": ["name", "fio"], "placeholder": ["фио", "фио*", "имя", "имя*"], "name": ["name", "fio"]}
        self.confirm = ["спасибо", "ваша заявка", "ожидайте", "менеджер", "перезвоним", "свяжется"]
        self.driver = driver
        self.getAttribute = lambda item: self.driver.execute_script('var items = {}; for (index = 0; index < '
                                                                    'arguments[0].attributes.length; ++index) { '
                                                                    'items[arguments[0].attributes[index].name] = '
                                                                    'arguments[0].attributes[index].value }; return '
                                                                    'items;', item)
        if xpath is not None:
            self.granddad = self.driver.find_element_by_xpath(xpath)
            args = self.granddad.find_elements_by_xpath(".//input")

        for arg in args:
            for key in self._name_.keys():
                if str.lower(arg.get_attribute(key)) in self._name_[key]:
                    self.name = arg
                    break
            for key in self._phone_.keys():
                if str.lower(arg.get_attribute(key)) in self._phone_[key]:
                    self.phone = arg
                    break
            for key in self._email_.keys():
                if str.lower(arg.get_attribute(key)) in self._email_[key]:
                    self.email = arg
                    break
        if self.granddad is None:
            self.granddad = args[0].find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..")
        try:
            self.button = self.granddad.find_element_by_xpath(".//button")
        except:
            try:
                items = self.granddad.find_elements_by_tag_name("input")
                for item in items:
                    if "отправить" in item.get_attribute("value").lower():
                        self.button = item
            except:
                print("кнопка не обнаружена")
        try:
            data_test = self.getAttribute(self.granddad)["data-test"]
            self.callButton = self.driver.find_element_by_xpath(f"//button[@data-test='{data_test}']")
        except Exception as e:
            pass
        if any(map(lambda i: i is None, (self.name, self.phone, self.button))):
            self.isready = False

    def action(self, obj, act: str, data=None):
        def do(obj, act, data):
            if act == "send_keys":
                obj.clear()
                obj.send_keys(data)
            elif act == "click":
                obj.click()

        self.driver.execute_script(f"window.scrollTo(0, {obj.location['y'] - 400});")
        for i in range(10):
            try:
                do(obj, act, data)
                return True
            except:
                sleep(0.1)
        do(obj, act, data)

    def Test(self, call_button=None):
        if self.isready:
            if self.callButton is not None:
                self.callButton.click()
            text_before = self.driver.find_element_by_xpath("//body").text
            if call_button is not None:
                self.action(obj=call_button, act="click")
            self.action(obj=self.name, act="send_keys", data=self.__nameDefault__)
            self.action(obj=self.phone, act="send_keys", data=self.__phoneDefault__[1:])
            if self.email is not None:
                self.action(obj=self.email, act="send_keys", data=self.__emailDefault__)
            self.driver.backend.storage.clear_requests()
            self.action(obj=self.button, act="click")
            request = self.findSendingRequest()
            sleep(8)
            # while True is None:
            #     sleep(2)
            # sleep(1)
            text_after = self.driver.find_element_by_xpath("//body").text
            _, txt_after = compareLists(str2list(text_before), str2list(text_after))
            confirmation = any([conf in txt.lower() for txt in txt_after for conf in self.confirm])
            if request is not None:
                body = request.response.body
            else:
                body = None
            try:
                content_encoding = request.response.headers["content-encoding"]
            except:
                content_encoding = None
            if content_encoding is not None:
                text = zlib.decompress(body, 16+zlib.MAX_WBITS).decode()
            else:
                text = unquote(body.decode())
            answer = any([conf in text for conf in self.confirm])
            return (confirmation and answer), confirmation, answer
        return None

    def findSendingRequest(self):
        for request in self.driver.requests:
            if request.response:
                if request.response.headers['Content-Type'] == 'text/html; charset=UTF-8':
                    try:
                        rt = ''.join(re.findall(r'[0-9]*', request.body.decode("utf-8")))
                        if rt != '':
                            if re.search(r'1234567890', rt).group(0) == '1234567890':
                                print(zlib.decompress(request.response.body, 16 + zlib.MAX_WBITS).decode())
                                return request
                    except:
                        continue
        return None