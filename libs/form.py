from time import sleep
from func4test import *


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
    # If form if ready for test
    ready = True

    def __init__(self, *args, xpath=None, **kwargs):
        """

        :param args: list of input tags if xpath == None
        :param xpath: xpath of form is included all input and button tags
        :param kwargs: driver -> selenium.webdriver
        """
        self.__emailDefault__ = "tester_form@gaps.edu.ru"
        self.__phoneDefault__ = "81234567890"
        self.__nameDefault__ = "Автотест"
        self._email_ = {"class": ["email", "e-mail"], "placeholder": ["email", "e-mail", "email*", "e-mail*"],
                        "name": ["email", "e-mail"]}
        self._phone_ = {"class": ["phone"], "placeholder": ["телефон", "телефон*"], "name": ["phone"]}
        self._name_ = {"class": ["name", "fio"], "placeholder": ["фио", "фио*", "имя", "имя*"], "name": ["name", "fio"]}
        self._statusMessage_ = {
            180: "Форма не детерминирована",
            480: "Кнопка вызова формы не кликабельна",
            481: "Не смог записать данные в поле Имя",
            482: "Не смог записать данные в поле Телефон",
            483: "Не смог записать данные в поле Email",
            484: "Кнопка отправки не кликабельна",
            491: "Некоректно введенное имя",
            492: "Некоректно введенный номер телефона",
            493: "Некоректно введенный email",
            280: "Все ок!",
            580: "Не найден никакой ответ от сервера",
            599: "Запрос не найден, сообщение не получено"
        }
        self.Driver = kwargs["driver"]
        self.getAttribute = lambda item: self.Driver.execute_script('var items = {}; for (index = 0; index < '
                                                                    'arguments[0].attributes.length; ++index) { '
                                                                    'items[arguments[0].attributes[index].name] = '
                                                                    'arguments[0].attributes[index].value }; return '
                                                                    'items;', item)
        if xpath is not None:
            self.granddad = self.Driver.find_element_by_xpath(xpath)
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
        if any(map(lambda i: i is None, (self.name, self.phone, self.button))):
            self.ready = False

    def action(self, obj, act: str, data=None):
        self.Driver.execute_script(f"window.scrollTo(0, {obj.location['y'] - 400});")
        for i in range(10):
            try:
                if act == "send_keys":
                    obj.clear()
                    obj.send_keys(data)
                elif act == "click":
                    obj.click()
                break
            except:
                sleep(0.1)

    def Test(self, call_button=None):
        if call_button is not None:
            try:
                self.action(call_button, "click")
            except Exception as e:
                return self.status(480, e, self.getAttribute(call_button))
        if self.ready:
            try:
                self.name.send_keys(self.__nameDefault__)
            except Exception as e:
                return self.status(481, e, self.name)
            try:
                self.phone.send_keys(self.__phoneDefault__)
            except Exception as e:
                return self.status(482, e, self.phone)
            if self.email is not None:
                try:
                    self.email.send_keys(self.__emailDefault__)
                except Exception as e:
                    return self.status(483, e, self.email)
            self.Driver.proxy.storage.clear_requests()
            try:
                self.action(obj=self.button, act="click")
            except Exception as e:
                return self.status(484, e, self.button)
            request = self.findSendingRequest()
            if request is not None:
                return self.status(request.response.status_code)
            else:
                return self.status(580)
        else:
            return self.status(180)

    def _Test(self, call_button=None):
        if self.ready:
            if call_button is not None:
                self.action(obj=call_button, act="click")
            self.action(obj=self.name, act="send_keys", data=self.__nameDefault__)
            self.action(obj=self.phone, act="send_keys", data=self.__phoneDefault__)
            if self.email is not None:
                self.action(obj=self.email, act="send_keys", data=self.__emailDefault__)
            self.action(obj=self.button, act="click")
            self.Driver.proxy.storage.clear_requests()
            request = self.findSendingRequest()
        return request.response.status_code

    def findSendingRequest(self):
        keys = ["email="+self.__emailDefault__[:self.__emailDefault__.find("@")]]
        sleep(5)
        for request in self.Driver.requests:
            if any([key in request.body.decode("utf-8", errors='ignore') for key in keys]) or any(
                    [key in request.querystring for key in keys]):
                return request
            else:
                return None

    def status(self, code, e=None, obj=None):
        try:
            message = self._statusMessage_[code]
        except:
            message = None
        return {"code": code, "message": message, "system error": e, "object": obj}

