import re
from time import time
from libs.pages.page import Page
from libs.pages.testpage import TestPage


class Form:
    granddad = None
    name = None
    phone = None
    email = None
    button = ".//button"
    callButton = None
    # If form if ready for test
    isready = True

    __emailDefault__ = "tester_form@gaps.edu.ru"
    __phoneDefault__ = "81234567890"
    __nameDefault__ = "Автотест"

    _email_ = {"class": ["email", "e-mail"], "placeholder": ["email", "e-mail", "email*", "e-mail*"],
               "name": ["email", "e-mail"]}
    _phone_ = {"class": ["phone"], "placeholder": ["телефон", "телефон*"], "name": ["phone"]}
    _name_ = {"class": ["name", "fio"], "placeholder": ["фио", "фио*", "имя", "имя*"], "name": ["name", "fio"]}
    confirm = ["спасибо", "ваша заявка", "ожидайте", "менеджер", "перезвоним", "свяжется", "отправлен"]


class PageForm(Page):

    def findform(self, *args, xpath=None, **kwargs):
        self.form = Form()
        xpath = self.__data2xpath__(xpath)
        if xpath is not None:
            self.form.granddad = self.findElement(xpath)
            args = self.findElements(element=self.form.granddad, xpath=f"({xpath})//input")
        self.form.name = self.selectElement(args, self.form._name_)
        self.form.phone = self.selectElement(args, self.form._phone_)
        self.form.email = self.selectElement(args, self.form._email_)
        if self.form.granddad is None:
            self.form.granddad = args[0].find_element("xpath", "..").find_element("xpath", "..").find_element("xpath",
                                                                                                              "..")
        try:
            data_test = self.attributes(self.form.granddad)["data-test"]
            self.form.callButton = f"//button[@data-test='{data_test}']"
        except Exception as e:
            pass
        if any(map(lambda i: i is None, (self.form.name, self.form.phone, self.form.button))):
            self.form.isready = False

    def Test(self):
        return self.Evaluation()

    def Evaluation(self):
        if self.form.callButton is not None:
            self.callPopup()
        text_before = self.text(xpath="//body")
        try:
            self.fillForm()
        except Exception as e:
            raise Exception(f"Не получилось заполнить форму: {e}")
        confirmation = self.waitEvaluation(text_before)
        return confirmation

    def callPopup(self):
        try:
            self.buttonCallPopup = self.findElement(self.form.callButton)
        except:
            self.buttonCallPopup = None
        if self.buttonCallPopup:
            try:
                self.buttonCallPopup.click()
            except Exception as e:
                raise Exception(f"Не удалось открыть поп-ап: {e}")

    def fillForm(self):
        self.fill(self.form.__nameDefault__, input=self.form.name)

        self.fill(self.form.__phoneDefault__, self.form.phone)
        self.sleep()
        value = ''.join(re.findall('[0-9]+', self.attribute(self.form.phone, 'value')))
        if value != self.form.__phoneDefault__:
            self.fill(self.form.__phoneDefault__[1:], self.form.phone)

        if self.form.email is not None:
            self.fill(self.form.__emailDefault__, input=self.form.email)
        button = self.findElement(xpath=".//button", element=self.form.granddad)
        self.click(elem=button)

    def waitEvaluation(self, text_before, timeout=10, delta=0.25):
        start = time()
        while time() - start < timeout:
            request = self.confirmationEvaluation(text_before)
            if request:
                return request
                break
            self.sleep(delta)
        raise TimeoutError("Запрос не найден")

    def confirmationEvaluation(self, text_before):
        text_after = self.text(xpath="//body")
        _, txt_after = compareLists(str2list(text_before), str2list(text_after))
        return any([conf in txt.lower() for txt in txt_after for conf in self.form.confirm])


def str2list(text):
    txt = []
    while True:
        ind = text.find("\n")
        if ind >= 0:
            if ind != 0:
                txt.append(text[:ind])
            text = text[ind + 1:]
        else:
            txt.append(text)
            break
    return txt


def compareLists(list1, list2):
    l1 = list1.copy()
    l2 = list2.copy()
    for l in list1:
        if l in l2:
            l2.remove(l)
    for l in list2:
        if l in l1:
            l1.remove(l)
    return l1, l2