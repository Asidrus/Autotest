from libs.pages.page import Page
from selenium.webdriver.support.ui import Select
from config import uploads_path


class PageMeetings(Page):
    meetingsButtonXpath = '//span[contains(text(),"Онлайн встречи")]/..'

    addEventButtonXpath = '//a[contains(text(),"Добавить событие")]'

    eventNameInputXpath = '//input[@id="id_name"]'
    groupSelectXpath = '//select[@id="id_courseid"]'
    yearSelectXpath = '//select[@id="id_date_year"]'
    typeSelectXpath = '//select[@id="id_type"]'

    addAttachmentXpath = '//a[contains(@title, "Добавить")]'
    uploadInputXpath = '//input[@name="repo_upload_file"]'
    uploadThisFileButtonXpath = '//button[contains(text(), "Загрузить")]'
    saveButtonXpath = '//input[@id="id_submitbutton"]'

    cancelButtonXpath = '//*[contains(text(), "2030 ")]/..//a[contains(@href,"cancel")]'
    acceptButtonXpath = '//button[@type="submit" and contains(text(), "Продолжить")]'

    def go2meeting(self):
        self.click(xpath=self.meetingsButtonXpath)

    def addEvent(self):
        self.click(xpath=self.addEventButtonXpath)
        self.fill('Тест', xpath=self.eventNameInputXpath)
        groupSelect = Select(self.findElement(self.groupSelectXpath))
        groupSelect.select_by_visible_text(groupSelect.options[1].text)

        yearSelect = Select(self.findElement(self.yearSelectXpath))
        yearSelect.select_by_value("2030")

        typeSelect = Select(self.findElement(self.typeSelectXpath))
        typeSelect.select_by_visible_text(typeSelect.options[1].text)

        self.click(xpath=self.addAttachmentXpath)

        from selenium.webdriver.remote.file_detector import LocalFileDetector

        input = self.findElement(self.uploadInputXpath)
        self.driver.execute_script("arguments[0].style.display = 'block';", input)
        self.driver.file_detector = LocalFileDetector()
        input.send_keys(uploads_path + "/blank.pdf")
        self.click(xpath=self.uploadThisFileButtonXpath)

        self.click(xpath=self.saveButtonXpath)

    def deleteEvent(self):
        self.click(xpath=self.cancelButtonXpath)
        self.click(xpath=self.acceptButtonXpath)
