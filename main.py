import json
from io import StringIO

import aiohttp
from lxml import etree

from config import *
import asyncio
from matplotlib import pyplot as plt
import random
from datetime import datetime, timedelta
from seleniumwire import webdriver

from func4test import GenData
from libs.aioparser import aioparser


async def main(links, pattern):
    res = {}
    for p in pattern:
        res[p] = []
    async with aiohttp.ClientSession() as session:
        i = 0
        for link in links:
            async with session.get(link["url"]) as response:
                print(i / len(links) * 100.0)
                i = i + 1
                try:
                    parser = etree.HTMLParser()
                    content = await response.content.read()
                    text = content.decode("windows-1251", errors='ignore')
                    tree = etree.parse(StringIO(text), parser=parser)
                    txt = etree.tostring(tree, method="text", encoding='windows-1251').decode("windows-1251")
                    for p in pattern:
                        if p in txt.lower():
                            res[p].append(link["url"])
                            print({p: link["url"]})
                    # if any([p in txt.lower() for p in pattern]):
                    #     res.append(link["url"]+"\n")
                except:
                    print("error")
    return res

def main2():
    parser = aioparser()
    parser.getAllUrls("https://mgaps.ru")
    pattern = ["707", "гуманитарн", "гапс", "академ", "мисао"]
    res = asyncio.run(main(parser.links, pattern))
    import json
    with open("temp.json", "w") as w:
        json.dump(res, w, indent=4)
    with open("temp.cache", "w") as w:
        data = []
        for key in res:
            for url in res[key]:
                if url not in data:
                    data.append(url+"\n")
        w.writelines(data)


def main3(site):
    domain = site.replace("https://", "").replace(".ru", "")
    fname = resources_path + f"/{domain}_form.json"
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
    fname = resources_path + f"/{domain}_form.json"

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
                    style = el[-1].getparent().getparent().get("style")
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

if __name__ == "__main__":
    # main4(sys.argv[1])
    aiop = aioparser()
    aiop.getAllUrls("https://niidpo.ru")
    urls = [link["url"] for link in aiop.links if "seminar" in link["url"]]
    asyncio.run(main5(urls))

