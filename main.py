from selenium import webdriver
from selenium.webdriver.common.by import By
from libs.form import DataToXpath, Form, PageForm


def main():
    driver = webdriver.Chrome("./chromedriver/chromedriver")
    try:
        driver.get("https://edu.i-spo.ru")
        form = driver.find_element(By.XPATH, "//form[@data-test='pop_form']")

        getAttribute = lambda item: driver.execute_script('var items = {}; for (index = 0; index < '
                                                          'arguments[0].attributes.length; ++index) { '
                                                          'items[arguments[0].attributes[index].name] = '
                                                          'arguments[0].attributes[index].value }; return '
                                                          'items;', item)
        xpath = DataToXpath({"tag": "form", "attrib": getAttribute(form)})
        print(xpath)
        form = Form(xpath=xpath, driver=driver)
        form.Test()

        # driver.find_element("xpath", "//button[@id='callback_btn']").click()
        # name = driver.find_element("xpath", "//input[@id='name_inline_556']")
        # name.send_keys("name")
        # phone = driver.find_element("xpath", "//input[@id='order_tel_556']")
        # phone.send_keys("1234567890")
        # import time
        # time.sleep(20)
    except Exception as e:
        raise e
    finally:
        driver.close()
        driver.quit()

def main2():
    url = "https://edu.i-spo.ru/seminar/ehkonomika-i-upravlenie-na-predpriyatii"
    datatest = "order_form"
    driver = webdriver.Chrome(executable_path="/home/kali/python/tests/chromedriver/chromedr")
    page = PageForm(driver)
    page.addCookie(url, {"name": "metric_off", "value": "1"})
    page.getPage(url)
    page.sleepPage(2)
    el = page.findElement(f"(//form[@data-test='{datatest}'])[1]")
    xpath = DataToXpath({"tag": "form", "attrib": page.getAttr(el)})
    page.findform(xpath=xpath)
    confirmation = page.Test()

if __name__ == "__main__":
    main2()
