import json
from io import StringIO
from time import time, sleep

import aiohttp
from lxml import etree
import os
from config import autotest_results
import asyncio
from matplotlib import pyplot as plt
import random
from datetime import datetime, timedelta
from seleniumwire import webdriver

from func4test import GenData, DataToXpath
from libs.aioparser import aioparser


def main3(site):
    domain = site.replace("https://", "").replace(".ru", "")
    fname = autotest_results + f"/{domain}_form.json"
    if os.path.exists(fname) and (
            (datetime.fromtimestamp(os.path.getmtime(fname)) - datetime.now()) < timedelta(days=1)):
        with open(fname, "r") as read_file:
            Data = json.load(read_file)
            read_file.close()
    else:
        parser = aioparser()
        parser.getAllUrls(site)
        urls = [link["url"] for link in parser.links]
        Data = {"data": GenData(urls)}
        with open(fname, "w") as write_file:
            json.dump(Data, write_file, indent=4)


def main4(site):
    domain = site.replace("https://", "").replace(".ru", "")
    fname = autotest_results + f"/{domain}_form.json"

    with open(fname, 'r') as r:
        data = json.load(r)
    DATA = []
    for d in data["data"]:
        flag = False
        for DD in DATA:
            if d["xpath"] == DD["xpath"]:
                flag = True
                continue
        if not flag:
            DATA.append(d)

    with open(fname, "w") as write_file:
        json.dump({"data": DATA}, write_file, indent=4)


async def main5(urls):
    parser = etree.HTMLParser()
    colors = []
    errors = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            url = url.strip()
            print(url)
            async with session.get(url) as response:
                content = await response.content.read()
                text = content.decode("windows-1251", errors='ignore')
                tree = etree.parse(StringIO(text), parser=parser)
                try:
                    el = tree.xpath("//sup[contains(text(),*)]")
                    parent = el[-1].getparent().getparent()
                    try:
                        if parent.get("class") == "note-star-block":
                            continue
                    except:
                        pass
                    style = parent.get("style")
                    color = style[style.find("background:")+12:]
                    color = color[:color.find(";")]
                    print(color)
                    if color not in colors:
                        colors.append(color)
                except Exception as e:
                    errors.append(url)
                    print("error"+str(e))
                # if "дополнительные требования" in txt.lower():
                #     tree = etree.parse(StringIO(text), parser=parser)
    print(colors)
    with open("resources/colors.tmp", "w") as w:
        w.writelines([(color+"\n") for color in colors])
    with open("resources/errors.tmp", "w") as w:
        w.writelines([(er + "\n") for er in errors])


def _filter(site):
    domain = site.replace("https://", "")
    with open(autotest_results+f"/{domain}_result.json", "r") as r:
        data = json.load(r)
    for d in data:
        if d == "4000 или 3 мес":
            continue
        data[d] = list(filter(lambda url: not any([(el in url) for el in ["/seminar", "/anons"]]), data[d]))
    with open(autotest_results+f"/{domain}_result.json", "w", encoding="utf-8") as w:
        json.dump(data, w, ensure_ascii=False, indent=4)


async def __genData(urls):
    parser = etree.HTMLParser()
    data = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as response:
                if "text/html" not in response.headers["Content-Type"]:
                    continue
                html = await response.text("utf-8", errors="ignore")
                tree = etree.parse(StringIO(html), parser=parser)
                forms = tree.xpath("//form[@data-test]")
                for el in forms:
                    if not any([(el.attrib["data-test"] == d["xpath"]["attrib"]["data-test"]) for d in data]):
                        data.append({"url": url, "xpath": {"tag": "form", "attrib": el.attrib}})
                    # xpath = DataToXpath({"tag": "form", "attrib": el.attrib})
                    # data.append({"url": url, "xpath": xpath})
                    # if not any([(d["xpath"] == xpath) for d in data]):
                    #     data.append()
    for d in data:
        d["xpath"] = DataToXpath(d["xpath"])
    return data


def fun():
    from seleniumwire import webdriver
    driver = webdriver.Chrome("./resources/chromedriver")
    # driver.get("https://sdo.niidpo.ru")
    driver.get("https://sdo.niidpo.ru/login/index.php")
    print(driver.requests[0].response.status_code)
    driver.close()
    driver.quit()


if __name__ == "__main__":
    # # _filter("https://niidpo.ru")
    # parser = aioparser()
    # parser.getAllUrls(site="https://edu.i-spo.ru")
    # data = asyncio.run(__genData([link["url"] for link in parser.links]))
    # for d in data:
    #     print(d)
    fun()
