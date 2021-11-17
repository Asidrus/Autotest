
from libs.search_content_ import main

def mgaps():
    pattern = ["гуманитарн", "гапс", "академ", "мисао", "мипк", "институт"]
    main("https://mgaps.ru", "windows-1251", pattern)


if __name__ == "__main__":
    fname_appendix = "_adaptive" if False else ""
    # pattern = ["гуманитарн", "гапс", "академ", "мисао", "мипк", "институт"]
    pattern = ["webp"]
    # main("https://mgaps.ru/", "windows-1251", pattern)
    main("https://psy.dev-u.ru", "utf-8", pattern)