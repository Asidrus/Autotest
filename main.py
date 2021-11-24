import logging
from time import sleep

from libs.network import Client
from libs.pages.testpage import TestPage
from libs.search_content_ import main

def mgaps():
    pattern = ["гуманитарн", "гапс", "академ", "мисао", "мипк", "институт"]
    main("https://mgaps.ru", "windows-1251", pattern)


if __name__ == "__main__":
    mgaps()

