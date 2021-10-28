from selenium import webdriver
from selenium.webdriver.common.by import By
from libs.form import DataToXpath, Form

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

if __name__ == "__main__":
    main()
