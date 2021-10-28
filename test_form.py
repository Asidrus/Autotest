import pytest
from time import sleep
from conf.config import WebdriverChrome
from sending_data import FillingInFieldsWithData


web_driver = WebdriverChrome()

send_data = FillingInFieldsWithData(web_driver.input_FCs, web_driver.btn, web_driver.driver, web_driver.text_err)

sleep(1)

send_data.get_data()
    
with allure.step(f"Посмотрим что получили"):
    with allure.step(f"Вложим шаги друг в друга по приколу"):
        with allure.step(f"Наверняка получится что-то интересное"):
            pass
    

# @pytest
@pytest.mark.parametrize("valid,result", send_data.get_data)
def test_A(valid, result):
    assert valid ^ result

assert "закрыто"
web_driver.closeDriver()