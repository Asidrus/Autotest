import asyncio
import sys

sys.path.append('/home/kali/autotest')
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


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)


headers = {
    "User-Agent": 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166'}


class aioparser:
    parser = None
    site = ''
    links = {"internal": [], "external": [], "resources": [], "errors": []}
    result = {}
    adaptive = False
    fname = ""
    autosave = True

    def __init__(self, site, pattern=None, adaptive=False, parse=False, autosave=True):
        self.site = site
        self.adaptive = adaptive
        self.headers = headers if adaptive else None
        self.parse = parse
        self.pattern = pattern
        self.autosave = autosave
        self.parser = etree.HTMLParser()
        self.getFileName()
        fnameLinks = self.fname + "_links.json"
        if (not parse) and (not pattern) and os.path.exists(fnameLinks) and (
                (datetime.now() - datetime.fromtimestamp(os.path.getmtime(fnameLinks))) < timedelta(hours=23)):
            self.readfile(fnameLinks)
        else:
            print(f"Файл {fnameLinks} не найден или страрый, начинаем парсинг ссылок, наливайте кофе... это надолго")
            self.links['internal'].append({"url": site, "from": []})
            asyncio.get_event_loop().run_until_complete(self.parsing())
            self.writefile(fnameLinks, self.links)
            if pattern:
                self.writefile(self.fname + "_result.json", self.result)

    def getFileName(self):
        start = [ind for ind in find_all(self.site, '/')][1] + 1
        end = [ind for ind in find_all(self.site, '.')][-1]
        self.fname = self.site[start:end] + self.fname_appendix if self.adaptive == True else self.site[start:end]
        self.fname = autotest_results + "/" + self.fname

    def readfile(self, fname, data):
        with open(fname, "r") as read_file:
            return json.load(read_file)

    def writefile(self, fname, data):
        with open(fname, "w") as write_file:
            json.dump(data, write_file, indent=4)

    def takeLink(self):
        yield from self.links['internal']

    async def parsing(self):
        async with aiohttp.ClientSession() as session:
            for link in self.takeLink():
                print(link["url"])
                try:
                    async with session.get(link["url"], headers=headers) as response:
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
                    self.links['errors'].append({"url": link["url"], "error": e})

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
                putInDict(url, link, self.links['internal'])
            elif url.startswith("http"):
                putInDict(url, link, self.links['external'])
            else:
                putInDict(url, link, self.links['resources'])

    async def search(self, html, link):
        html = html.lower()
        for p in self.pattern:
            if p.lower() in html:
                self.result[p].append(link["url"])
                # print({p: link["url"]})


if __name__ == '__main__':
    parser = aioparser('https://pentaschool.ru', ['витковский'], parse=True)
