from func4test import GenData
import json
import sys
sys.path.append("/home/kali/autotest/")

from libs.aioparser import aioparser
parser = aioparser()
parser.getAllUrls('https://mgaps.ru')

data = GenData([link['url'] for link in parser.links])

mass = []

for form in data:
   flag = False
   for m in mass:
       if m['xpath'] == form['xpath']:
           flag = True
           break
   if not flag:
       mass.append(form)

with open('mgaps.json', "w", encoding='utf-8') as file:
    json.dump({"data": mass}, file, indent=4, ensure_ascii=False)





