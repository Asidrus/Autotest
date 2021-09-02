from seleniumwire import webdriver
from libs.form import Form
from time import sleep
import allure

def _test():
    from func4test import _urlsParser, GenData
    import json
    # data = _urlsParser("https://pentaschool.ru", parse=False)
    # urls = [link["url"] for link in data["links"]]
    # gendata = GenData(urls)
    # with open(f"forms.json", "w") as write_file:
    #     json.dump({"data": gendata}, write_file, indent=4)

    with open("forms.json", "r") as read_file:
        Data = json.load(read_file)
        read_file.close()
    data = []
    for item in Data["data"]:
        if data == 0:
            data.append(item)
        else:
            count = 0
            if len([True for dat in data if dat["xpath"] == item["xpath"]]) == 0:
                data.append(item)
    result = [(item["url"], item["xpath"]) for item in data]
    print(result)
    print(len(result))


# def wrapper(func, error=None, screenshot=None, **kwargs):
#     try:
#         func(**kwargs)
#     except Exception as e:
#         if screenshot:
#             allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
#         if error is None:
#             print(e)
#         else:
#             print(error)


def wrapper(*args, error=None, screenshot=None, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as e:
        # if screenshot:
        #     allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
        if error is None:
            raise e
        else:
            raise Exception(error)


def step(func):
    def wrapper(*args, error=None, screenshot=None, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            # if screenshot:
            #     allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
            if error is None:
                raise e
            else:
                raise Exception(error)
    return wrapper

@step
def div(b, c):
    a = b / c
    print(a)


if __name__ == "__main__":
    # div(10,0, error="деление")
    step(div)(10, 10)
    # _test()
