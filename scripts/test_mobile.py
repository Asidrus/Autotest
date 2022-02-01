from appium import webdriver
from selenium.webdriver.common.by import By

from time import sleep


def findElementFromList(driver, className, attr, value):
    elements = driver.find_elements(By.CLASS_NAME, className)
    for element in elements:
        if element.get_attribute(attr) == value:
            return element
    return None


desired_capabilities = {
    "platformName": "Android",
    "platformVersion": "11",
    "deviceName": "Pixel 5 API 30",
    "app": "/home/kali/autotest/Система обучения АкадемСити_1.5.2_apkcombo.com.apk",
    "automationName": "UiAutomator2",
}

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_capabilities=desired_capabilities)

sleep(5)

inputs = driver.find_elements(By.CLASS_NAME, "android.widget.EditText")

login = inputs[0]
password = inputs[1]
button = findElementFromList(driver, 'android.widget.Button', 'content-desc', 'Войти')

login.click()
sleep(0.1)
login.send_keys("katyashikhova@mail.ru")

password.click()
sleep(0.1)
password.send_keys("123123")

sleep(0.1)
button.click()
sleep(5)
driver.hide_keyboard()
sleep(50)

