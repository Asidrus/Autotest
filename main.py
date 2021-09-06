from seleniumwire import webdriver
from libs.form import Form
from time import sleep
import allure
from func4test import urlsParser, GenData
from datetime import datetime, timedelta
import os
import json

path = os.path.abspath(os.getcwd())


def main():
    site = "https://pentaschool.ru"
    domain = site.replace("https://", "").replace(".ru", "")
    fname = path + "/resources/" + f"{domain}_form.json"

    if os.path.exists(fname) and (
            (datetime.fromtimestamp(os.path.getmtime(fname)) - datetime.now()) < timedelta(days=1)):
        with open(fname, "r") as read_file:
            Data = json.load(read_file)
            read_file.close()
    else:
        data = urlsParser("https://pentaschool.ru", parse=True)
        urls = [link["url"] for link in data["links"]]
        Data = {"data": GenData(urls)}
        with open(fname, "w") as write_file:
            json.dump(Data, write_file, indent=4)

    data = []
    for item in Data["data"]:
        if data == 0:
            data.append(item)
        else:
            if len([True for dat in data if dat["xpath"] == item["xpath"]]) == 0:
                data.append(item)
    result = [(item["url"], item["xpath"]) for item in data]
    print(result)


if __name__ == "__main__":
    main()
