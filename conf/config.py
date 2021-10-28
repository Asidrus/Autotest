from selenium import webdriver
from time import sleep


class WebdriverChrome:

    def __init__(self):
        self.driver = webdriver.Chrome("/home/evgenii/python/conf/chromedriver")
        self.website = "https://pentaschool.ru/program/program-graficheskij-dizajn-v-reklame-s-nulya"
        self.text_err = "//div[@class='form_errors']"
        self.driver.get(self.website)
        self.input_FCs = self.driver.find_element_by_xpath("//input[@class='els-form gtm_diplom_form']")
        self.btn = self.driver.find_element_by_xpath("//button[@class='but-cons amber-but']")


    def closeDriver(self):
        self.driver.close()
        self.driver.quit()
