import json
import os
from libs.case import *
import smtplib
from lxml import etree
from io import StringIO
import requests

path = os.path.abspath(os.getcwd())


def DataToXpath(data):
    atts = ''
    for att in data["attrib"].keys():
        atts = atts + f" and @{att}='{data['attrib'][att]}'"
    atts = '[' + atts[5:] + ']'
    return f"//{data['tag']}{atts}"


def sendReportOnEmail(to: str, title, msg):
    # login = "tester3@gaps.edu.ru"
    # password = None
    # server = "smtp.yandex.ru"
    login = "asidruswork@gmail.com"
    password = "33Ns3LZP"
    server = "smtp.gmail.com"
    if True:
        smtp = smtplib.SMTP_SSL(server, 465)
        smtp.login(login, password)
    else:
        smtp = smtplib.SMTP(server, 587)
        smtp.starttls()
        smtp.login(login, password)

    message = f"From: {login}\r\nTo: {to}\r\nContent-Type: text/plain; charset='utf-8'\r\nSubject: {title}\r\n\r\n" + msg
    smtp.sendmail(login, to, msg.encode("utf8"))
    smtp.quit()


class ErrorParser:
    IsCorrect = 0
    IncorrectName = 1
    IncorrectPhone = 2
    IncorrectEmail = 3
    NotAllFieldsAreFilled = 4

    def __init__(self):
        self.typeError = {
            "name": self.IncorrectName,
            "phone": self.IncorrectPhone,
            "email": self.IncorrectEmail
        }

    def ParseError(self, texterror):

        Errors = list()
        TextError = str.lower(texterror)
        if len(TextError) > 0:
            if ("звезд" in TextError) | ("звёзд" in TextError):
                Errors.append(self.NotAllFieldsAreFilled)
            if "имя" in TextError:
                Errors.append(self.IncorrectName)
            if ("номер" in TextError) | ("телеф" in TextError):
                Errors.append(self.IncorrectPhone)
            if ("email" in TextError) | ("e-mail" in TextError):
                Errors.append(self.IncorrectEmail)
        else:
            Errors.append(self.IsCorrect)
        return Errors


def str2list(text):
    txt = []
    while True:
        ind = text.find("\n")
        if ind >= 0:
            if ind != 0:
                txt.append(text[:ind])
            text = text[ind + 1:]
        else:
            txt.append(text)
            break
    return txt


def compareLists(list1, list2):
    l1 = list1.copy()
    l2 = list2.copy()
    for l in list1:
        if l in l2:
            l2.remove(l)
    for l in list2:
        if l in l1:
            l1.remove(l)
    return l1, l2


def genCasesForFormValidation(fname):
    with open(fname, "r") as read_file:
        Data = json.load(read_file)
    Cases = {}
    for url in Data["Tests"]:
        for form in url["form"]:
            for valid in form["valid"]:
                try:
                    if Cases[valid] is None:
                        pass
                except:
                    Cases[valid] = ReadCases(**Data["Cases"][valid])
                for case in Cases[valid]:
                    yield {
                        "url": url["url"],
                        "xpath": form["xpath"],
                        "valid": valid,
                        "case": case
                    }


def GenData(urls):
    data = []
    parser = etree.HTMLParser()
    getGrandDad = lambda item: item.xpath("..")[0].xpath("..")[0].xpath("..")[0]
    count = 0
    for url in urls:
        count = count + 1
        print(int(count / len(urls) * 10000) / 100)
        try:
            page = requests.get(url, verify=True)
            if "text/html" not in page.headers["Content-Type"]:
                continue
            html = page.content.decode("utf-8", errors='ignore')
            tree = etree.parse(StringIO(html), parser=parser)
            inputs = tree.xpath("(//input)")
            for input in inputs:
                if input.get("type") == 'hidden':
                    inputs.remove(input)
            groups = [[]]
            for i in range(len(inputs)):
                if i == 0:
                    groups[0].append(i + 1)
                elif getGrandDad(inputs[i]) == getGrandDad(inputs[i - 1]):
                    groups[-1].append(i + 1)
                else:
                    groups.append([i + 1])
            groups = list(filter(lambda group: len(group) > 1, groups))
            data = data + [{"url": url, "xpath": DataToXpath(
                {"tag": getGrandDad(inputs[group[0]]).tag, "attrib": getGrandDad(inputs[group[0]]).attrib})} for group
                           in
                           groups]
        except Exception as e:
            print(e)
    return data


# async def main2(links):
#     async with aiohttp.ClientSession() as session:
#         i = 0
#         for link in links:
#             async with session.get(link["url"]) as response:
#                 print(i/len(links)*100.0)
#                 i = i+1
#                 try:
#                     parser = etree.HTMLParser()
#                     content = await response.content.read()
#                     text = content.decode("windows-1251", errors='ignore')
#                     tree = etree.parse(StringIO(text), parser=parser)
#                     txt = etree.tostring(tree, method="text", encoding='windows-1251').decode("windows-1251")
#                     if any([number in txt.lower() for number in ("0010006", "0008663")]):
#                         res.append(link["url"]+"\n")
#                 except:
#                     pass
#
#     return res