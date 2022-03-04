from libs.pages.page import Page


class PageLogin(Page):

    _name_ = {"name": ["username"]}
    _password_ = {"name": ["password"]}
    _button_ = {"type": ["submit"]}

    documentsButtonXpath = '//li[contains(@class, "myprograms") and contains(@class, "active")]//span[contains(text(),"Документы")]'

    def login(self, login, password, checkboxes=None):
        self.fill(login, input=self.selectElement(self.findElements("//input"), self._name_))
        self.fill(password, self.selectElement(self.findElements("//input"), self._password_))

        for checkbox in checkboxes:
            self.click(xpath=checkbox)

        self.click(self.selectElement(self.findElements("//button"), self._button_))

    def go2documents(self):
        self.click(xpath=self.documentsButtonXpath)




