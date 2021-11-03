# class A:
#     def func1(self):
#         print("func1")
#     def __init__(self):
#         print("setup driver")

# class B(A):
#     def func2(self):
#         print("func2")
#     def __init__(self):
#         super().__init__()

# class C(B):
#     def func3(self):
#         print("func3")
        
#     def __init__(self) -> None:
#         super().__init__()
#         self.func1()
#         self.func2()

# cc = C()

from libs.baseApp import WorkDriver
from selenium import webdriver
from libs.form import PageForm
from libs.func4test import DataToXpath

driver = webdriver.Chrome("/home/ta-tyan/Документы/py/Tests/chromedr")
page = PageForm(driver)
page.getPage("https://edu.i-spo.ru")
datatest = "consultant_form_g"
el = page.findElement(f"(//form[@data-test='{datatest}'])[1]")
xpath = DataToXpath({"tag": "form", "attrib": page.getAttr(el)})
page.findform(xpath=xpath)

page.Test()
page.sleepPage(10)