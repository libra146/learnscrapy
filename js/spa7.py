import json
import re

import requests

res = requests.get('https://spa7.scrape.center/js/main.js').text
content = re.findall('players = (\[[\s\S]+\])', res)[0]  # type:str
json_content = json.loads(content.replace('\'', '"')
                          .replace('name', '"name"')
                          .replace('image', '"image"')
                          .replace('birthday', '"birthday"')
                          .replace('height', '"height"')
                          .replace('weight', '"weight"')
                          .replace('},\n', '}\n'))
for a in json_content:
    print(a)
