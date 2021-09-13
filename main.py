from datetime import datetime
import aiohttp
import asyncio
from lxml import etree
from io import StringIO
import requests


async def get_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response
            # parser = etree.HTMLParser()
            # html = response.text()
            # tree = etree.parse(StringIO(html), parser=parser)
            # a_tags = tree.xpath("//a[@href]")

async def urlsParser_async(site: str):
    def putInDict(url, link, dictionary):
        flag = False
        for _link in dictionary:
            if _link["url"] == url:
                flag = True
                if link["url"] not in _link["from"]:
                    _link["from"].append(link["url"])
                break
        if not flag:
            dictionary.append({"url": url, "from": [link["url"]]})

    links = [{"url": site, "from": []}]
    redirect = []
    others = []
    parser = etree.HTMLParser()
    for link in links:
        print(link["url"])
        async with aiohttp.ClientSession() as session:
            async with session.get(link["url"]) as response:
                if "text/html" not in response.headers["Content-Type"]:
                    continue
                html = await response.text("utf-8", errors="ignore")
                tree = etree.parse(StringIO(html), parser=parser)

        a_tags = tree.xpath("//a[@href]")
        for a in a_tags:
            url = a.get("href", "")
            if url in ("", "/", link["url"], link["url"] + "/") or url.startswith("#"):
                continue
            if url.startswith("/"):
                url = site + url
                putInDict(url, link, links)
            elif url.startswith("http"):
                putInDict(url, link, redirect)
            else:
                putInDict(url, link, others)
    return {"links": links, "redirect": redirect, "others": others}


def urlsParser(site: str):
    def putInDict(url, link, dictionary):
        flag = False
        for _link in dictionary:
            if _link["url"] == url:
                flag = True
                if link["url"] not in _link["from"]:
                    _link["from"].append(link["url"])
                break
        if not flag:
            dictionary.append({"url": url, "from": [link["url"]]})

    links = [{"url": site, "from": []}]
    redirect = []
    others = []
    parser = etree.HTMLParser()
    for link in links:
        print(link["url"])
        page = requests.get(link["url"])
        if "text/html" not in page.headers["Content-Type"]:
            continue
        html = page.content.decode("utf-8", errors='ignore')
        tree = etree.parse(StringIO(html), parser=parser)
        a_tags = tree.xpath("//a[@href]")
        for a in a_tags:
            url = a.get("href", "")
            if url in ("", "/", link["url"], link["url"] + "/") or url.startswith("#"):
                continue
            if url.startswith("/"):
                url = site + url
                putInDict(url, link, links)
            elif url.startswith("http"):
                putInDict(url, link, redirect)
            else:
                putInDict(url, link, others)
    return {"links": links, "redirect": redirect, "others": others}


async def get_page_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://niidpo.ru') as response:
            pass


async def GETPAGE(func, url, *args, **kwargs):
    async def wrapper():
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                res = await func(url, response, *args)
        return res
    return wrapper

@GETPAGE
async def getattr(url, response):
    html = await response.text("utf-8", errors="ignore")
    tree = etree.parse(StringIO(html), parser=parser)
    a_tags = tree.xpath("//a[@href]")



if __name__ == "__main__":
    start = datetime.now()
    from libs.aioparser import aioparser
    parser = aioparser()
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(urlsParser_async("https://pentaschool.ru"))
    loop.run_until_complete(parser.parse("https://pentaschool.ru"))
    # urlsParser("https://pentaschool.ru")
    print(datetime.now()-start)
