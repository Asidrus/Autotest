from libs.pages.page import Page


class PageLogin(Page):

    _name_ = {"name": ["username"]}
    _password_ = {"name": ["password"]}
    _button_ = {"type": ["submit"]}

    def login(self, login, password):
        self.fill(login, input=self.selectElement(self.findElements("//input"), self._name_))
        self.fill(password, self.selectElement(self.findElements("//input"), self._password_))
        # self.click(xpath="//button[@type='submit']")
        self.click(self.selectElement(self.findElements("//button"), self._button_))