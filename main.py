from seleniumwire import webdriver
from libs.form import Form
from time import sleep
import allure
from func4test import urlsParser, GenData
from datetime import datetime, timedelta
import os
import json

path = os.path.abspath(os.getcwd())


def test_ADPO():




if __name__ == "__main__":
    # main()
    site = "https://adpo.edu.ru"
    data = urlsParser(site, parse=True)