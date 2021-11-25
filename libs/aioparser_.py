import asyncio
import aiohttp
import os
import json
from io import StringIO
from lxml import etree
from datetime import datetime, timedelta
from config import autotest_results


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


headers = {"User-Agent": 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166'}


class aioparser:

    parser = etree.HTMLParser()
    site = ''
    links = []
    redirect = []
    others = []
    errors = []
    result = {}
    adaptive = False
    fname_appendix = ""

    def __init__(self, site, pattern=None, adaptive=False, parse=False):
        self.site = site
        self.adaptive = adaptive
        self.parse = parse
        self.pattern = pattern
        pass


    def getAllUrls(self, site, parse=False, adaptive=False):
        self.adaptive = adaptive
        self.fname_appendix = "_adaptive" if adaptive == True else ""
        fname = autotest_results + "/" + site.replace('https://', '').replace('.ru', '') + self.fname_appendix + "_links.json"
        if (not parse) and os.path.exists(fname) and (
                (datetime.now() - datetime.fromtimestamp(os.path.getmtime(fname))) < timedelta(hours=23)):
            self.readfile(fname)
        else:
            print(f"Файл {fname} не найден или страрый, начинаем парсинг ссылок, наливайте кофе... это надолго")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.parse(site))
            self.writefile(fname)

    def readfile(self, fname):
        with open(fname, "r") as read_file:
            Data = json.load(read_file)
            read_file.close()
            self.links = Data["links"]
            self.redirect = Data["redirect"]
            self.others = Data["others"]

    def writefile(self, fname):
        with open(fname, "w") as write_file:
            json.dump(
                {"links": self.links, "redirect": self.redirect, "others": self.others},
                write_file,
                indent=4)

    def takeLink(self):
        yield from self.links

    async def parse(self, site):
        self.links.append({"url": site, "from": []})
        async with aiohttp.ClientSession() as session:
            for link in self.takeLink():
                print(link["url"])
                try:
                    async with session.get(link["url"], allow_redirects=True) as response:
                        header = response.headers["Content-Type"]
                        if "text/html" not in header:
                            continue
                        encoding = header[header.find("=") + 1:]
                        html = await response.text(encoding, errors="ignore")
                        if self.parse:
                            await self.getLinks(html, link)
                        if self.pattern:
                            await self.search(html, link)
                except Exception as e:
                    self.errors.append({"url": link["url"], "error": e})

    async def getLinks(self, html, link):
        tree = etree.parse(StringIO(html), parser=self.parser)
        a_tags = tree.xpath("//a[@href]")
        for a in a_tags:
            url = a.get("href", "")
            if url in ("", "/", link["url"], link["url"] + "/", link["url"].replace(self.site, "")) or ("#" in url) or (
                    "?" in url):
                continue
            if url.startswith("/"):
                url = self.site + url
                putInDict(url, link, self.links)
            elif url.startswith("http"):
                putInDict(url, link, self.redirect)
            else:
                putInDict(url, link, self.others)

    async def search(self, html, link):
        html = html.lower()
        for p in self.pattern:
            if p.lower() in html:
                self.result[p].append(link["url"])
                print({p: link["url"]})