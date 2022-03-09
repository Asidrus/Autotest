from libs.pages.page import Page


class PageLecture(Page):

    courseXpath = '(//td[@aria-label="Дисциплина"])[1]/a'
    lectureXpath = '(//span[contains(text(),"Тема")]/..)[1]'
    nextButtonXpath = '//a[@id="next"]'
    backButtonXpath = '//a[@id="back"]'
    fullScreenButtonXpath = '//a[@id="fullscreen"]'
    downloadLectureXpath = '//a[@id="download"]'

    def go2lecture(self):
        self.click(xpath=self.courseXpath)
        self.click(xpath=self.lectureXpath)

    def downloadLecture(self):
        self.click(xpath=self.downloadLectureXpath)

    def nextPage(self):
        elem = self.findElement(self.nextButtonXpath)
        self.sleep(3)
        self.driver.execute_script(f"window.scrollTo(0, {elem.location['y'] - 400})")
        self.click(elem)

    def backPage(self):
        elem = self.findElement(self.backButtonXpath)
        self.sleep(3)
        self.driver.execute_script(f"window.scrollTo(0, {elem.location['y'] - 400})")
        self.click(elem)

    def fullScreenWindow(self):
        self.click(xpath=self.fullScreenButtonXpath)