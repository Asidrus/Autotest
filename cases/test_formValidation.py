import allure
from allure_commons.types import AttachmentType
import pytest
import os
import json
from libs.func4test import genCasesForFormValidation
from libs.func4test import compareLists,str2list
from libs.form import Form
from libs.form import ErrorParser

path = os.path.abspath(os.getcwd())


def pytest_generate_tests(metafunc):
    if "fn" in metafunc.fixturenames:
        with open(metafunc.config.getoption("fn"), "r") as read_file:
            Data = json.load(read_file)
        metafunc.parametrize("url", urls)




@allure.feature("Тестирование форм")
@allure.story("Валидация")
@allure.severity("Major")
@pytest.mark.parametrize("data", genCasesForFormValidation(path + "/resources/FormValidation.json"))
def test_formValidation(setup_driver, data):
    Driver = setup_driver
    if Driver.current_url is not None:
        if Driver.current_url != data["url"]:
            Driver.get(data["url"])
    parent = Driver.find_element_by_xpath(data["xpath"])
    inputs = parent.find_elements_by_xpath(".//input")
    form = Form(*inputs, driver=Driver)
    errp = ErrorParser()
    text1 = Driver.find_element_by_xpath(data["xpath"]).text
    send = {"name": form.name.send_keys,
            "phone": form.phone.send_keys,
            "email": form.email.send_keys}
    clear = {"name": form.name.clear,
             "phone": form.phone.clear,
             "email": form.email.clear}
    send[data["valid"]](data["case"].Value)
    form.button.click()
    text2 = Driver.find_element_by_xpath(data["xpath"]).text
    clear[data["valid"]]()
    txt2 = compareLists(str2list(text1), str2list(text2))
    txt = ""
    for _txt in text2:
        txt += _txt
    err = errp.ParseError(txt)
    assert (errp.typeError[data["valid"]] in err) ^ data["case"].Valid, f"{data}, case = {data['case'].__str__()}"
