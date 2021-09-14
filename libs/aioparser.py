import asyncio
from io import StringIO

import aiohttp
from lxml import etree


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


async def getpage(func, *args, **kwargs):

    async def wrapper():
        func(*args)
    return wrapper


class aioparser:

    parser = None

    links = []
    redirect = []
    others = []

    def takeLink(self):
        yield from self.links

    async def _parse(self, site):
        self.links.append({"url": site, "from": []})
        async with aiohttp.ClientSession() as session:
            for link in self.takeLink():
                print(link["url"])
                async with session.get(link["url"]) as response:
                    if "text/html" not in response.headers["Content-Type"]:
                        continue
                    text = await response.text()
                    html = await response.text("utf-8", errors="ignore")
                    tree = etree.parse(StringIO(html), parser=self.parser)



    async def parse(self, site):
        links = [{"url": site, "from": []}]
        redirect = []
        others = []
        parser = etree.HTMLParser()

        for link in links:
            print(link["url"])
            response = await self.getpage(link["url"])
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


