import os
from time import time

from config import downloads_path
from libs.pages.page import Page


class PageDocuments(Page):

    activePopupXpath = '//div[contains(@class, "modal") and contains(@class, "show")]'
    closePopupButtonXpath = '//button[contains(@class, "buttonNo")]'

    payButtonXpath = '//input[@id="pay_online_btn"]'
    payButtonOnSiteXpath = '//input[@class="payment-button"]'

    downloadTicketButton = '//a[contains(text(), "Скачать квитанцию")]'

    def closePopUp(self):
        try:
            popup = self.findElement(self.activePopupXpath)
        except:
            pass
        if popup is not None:
            self.click(xpath=self.activePopupXpath+self.closePopupButtonXpath)

    def go2payment(self):
        self.click(xpath=self.payButtonXpath)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.click(xpath=self.payButtonOnSiteXpath)

    def downloadTicket(self):
        self.click(xpath=self.downloadTicketButton)

    def findDownloadedFile(self):
        start = time()
        while (time() - start) < 10:
            if any(map(lambda x: ".rtf" in x, os.listdir(downloads_path))):
                return True
            self.sleep()