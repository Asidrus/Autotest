import sys
import pathlib
path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.insert(-1, path)
import json
from io import StringIO
import aiohttp
from lxml import etree
from config import autotest_results
import asyncio
from aioparser import aioparser


# autotest_results = "/home/kali/autotest-results"

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166'}
fname_appendix = ""


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)


async def searcher(links, pattern, encoding):
    res = {}
    for p in pattern:
        res[p] = []
    async with aiohttp.ClientSession() as session:
        i = 0
        for link in links:
            # менять
            async with session.get(link["url"], headers=headers) as response:
                print(i / len(links) * 100.0)
                i = i + 1
                parser = etree.HTMLParser()
                content = await response.content.read()
                txt = content.decode(encoding, errors='ignore')
                for p in pattern:
                    if p in txt.lower():
                        if p == "рассрочка":
                            # менять
                            if len([el for el in find_all(txt.lower(), p)]) < 3:
                                continue
                        if p in ["справк", "копи", "продлить", "увеличить", "рассрочка"]:
                            if any([(el in link["url"]) for el in ["/seminar", "/anons"]]):
                                continue
                        if p == "4000":
                            if (len([el for el in find_all(txt.lower(), p)]) == 1) and ("}, 4000" in txt.lower()):
                                continue
                        res[p].append(link["url"])
                        print({p: link["url"]})
    return res


def main(site, encoding, pattern):
    parser = aioparser()
    parser.getAllUrls(site, adaptive=True)
    res = asyncio.run(searcher(parser.links, pattern, encoding))

    with open(autotest_results + f"/{site.replace('https://', '').replace('https://', '')}{fname_appendix}_result.json",
              "w", encoding="utf-8") as w:
        json.dump(res, w, indent=4, ensure_ascii=False)
    with open(autotest_results + f"/{site.replace('https://', '').replace('https://', '')}{fname_appendix}_result.txt",
              "w") as w:
        data = []
        for key in res:
            for url in res[key]:
                if url not in data:
                    data.append(url + "\n")
        w.writelines(data)


if __name__ == "__main__":
    # res = asyncio.run(searcher([{"url": "https://niidpo.ru/korporativnoe_obuchenie"}], ["4000"], "windows-1251"))
    #менять
    fname_appendix = "_adaptive" if True else ""
    pattern = ["следующей"]
    main(sys.argv[1], "windows-1251", pattern)