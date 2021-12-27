import asyncio
import aiohttp
import os
import sys
sys.path.append('/home/kali/autotest/')
import json
from io import StringIO
from lxml import etree
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from config import *
STORAGE_PATH = autotest_results+'/'

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
    fnameLinks = ''
    fnameResults = ''
    autosave = True

    def __init__(self, site, pattern=None, adaptive=False, parse=False, autosave=True):
        inds = [ind for ind in find_all(site, '/')]
        if len(inds) > 2:
            self.site = site[:[ind for ind in find_all(site, '/')][2]]
        else:
            self.site = site
        self.adaptive = adaptive
        self.headers = headers if adaptive else None
        self.parse = parse
        self.pattern = pattern
        self.autosave = autosave
        self.parser = etree.HTMLParser()
        self.getFileName()

    def __str__(self):
        return f"site='{self.site}', pattern='{self.pattern}'"

    async def run(self):
        if os.path.exists(self.fnameLinks) and ( #and (not self.pattern)
                (datetime.now() - datetime.fromtimestamp(os.path.getmtime(self.fnameLinks))) < timedelta(hours=23)):
            self.readfile(self.fnameLinks)
        else:
            print(
                f"Файл {self.fnameLinks} не найден или страрый, начинаем парсинг ссылок, наливайте кофе... это надолго")
            self.links = {"internal": [], "external": [], "resources": [], "errors": []}
            self.links['internal'] = [{"url": self.site, "from": []}]
            self.result = {}
            for p in self.pattern:
                self.result[p] = []
            await self.parsing()
            self.writeResults()

    def writeResults(self):
        self.writefile(self.fnameLinks, self.links)
        if self.pattern:
            self.writefile(self.fnameResults, self.result)

    def getFileName(self):
        start = [ind for ind in find_all(self.site, '/')][1] + 1
        end = [ind for ind in find_all(self.site, '.')][-1]
        domain = self.site[start:end] + "_adaptive" if self.adaptive == True else self.site[start:end]
        self.fnameLinks = STORAGE_PATH + domain + "_links.json"

        if (type(self.autosave) == bool) and (self.autosave == True):
            self.fnameResults = STORAGE_PATH + domain + "_result.json"
        else:
            self.fnameResults = STORAGE_PATH + self.autosave + '.json'

    def readfile(self, fname):
        with open(fname, "r") as read_file:
            self.links = json.load(read_file)

    def writefile(self, fname, data):
        with open(fname, "w", encoding='utf-8') as write_file:
            json.dump(data, write_file, indent=4, ensure_ascii=False)
            print(f'сохранил файл в {fname}')

    def takeLink(self):
        yield from self.links['internal']

    async def parsing(self):
        async with aiohttp.ClientSession() as session:
            for link in self.takeLink():
                # print(link["url"])
                try:
                    async with session.get(link["url"], headers=headers) as response:
                        header = response.headers["Content-Type"]
                        if "text/html" not in header:
                            continue
                        encoding = header[header.find("=") + 1:]
                        try:
                            html = await response.text(encoding, errors="ignore")
                        except Exception as e:
                            html = await response.text('windows-1251', errors="ignore")
                            print(f"Ошибка в кодировке {e} {link['url']} {encoding} {response.headers['Content-Type']}")
                        try:
                            if self.parse:
                                await self.getLinks(html, link)
                        except Exception as e:
                            print(f"Ошибка в парсинге {e} {link['url']}")
                        try:
                            if self.pattern and ('seminar' in link['url']):
                                await self.search(html, link)
                        except Exception as e:
                            print(f"Ошибка в поиске {e} {link['url']}")
                except Exception as e:
                    self.links['errors'].append({"url": link["url"], "error": str(e)})
                    print({"url": link["url"], "error": str(e)})

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
        soup = BeautifulSoup(html, "lxml")
        a_tag = soup.find('div', attrs={'class': 'header-elems_logo'}).find("a")
        try:
            res = a_tag.find("a")
            self.result["a"].append(link["url"])
            print(link["url"])
        except:
            pass


def main():
    import requests
    res = requests.get("https://niidpo.ru/news/1044", headers=headers)
    html = res.text
    if '<a href="/view/adaptiv/assets/images_5/logo-new5.png">' in html:
        print('dya')
    else:
        print('net')


if __name__ == '__main__':
    parser = aioparser('https://niidpo.ru', ['3 мес', '4000'], parse=True)
    asyncio.run(parser.run())
    asyncio.run(main())
    # main()