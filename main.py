import logging
from time import sleep

from libs.network import Client
from libs.pages.testpage import TestPage
from libs.search_content_ import main


import sys

if __name__ == "__main__":
    # pattern = ["бессрочн", "библиоклуб", "biblioclub"]
    pattern = ['образца']
    main(sys.argv[1], "windows-1251", pattern)

