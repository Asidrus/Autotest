from func4test import GenData
import json
import sys
sys.path.append("/home/kali/autotest/")

from libs.aioparser import aioparser
parser = aioparser()
parser.getAllUrls('https://vgaps.ru')

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

with open('forms.json', "w") as file:
    json.dump({"data": mass}, file)





