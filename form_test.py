from test_form import FillingInFieldsWithData
from time import sleep
from conf.config import WebdriverChrome
from sending_data import FillingInFieldsWithData


web_driver = WebdriverChrome()

send_data = FillingInFieldsWithData(web_driver.input_FCs, web_driver.btn, web_driver.driver, web_driver.text_err)

sleep(1)

send_data.get_data()
    
assert "закрыто"

web_driver.closeDriver()


