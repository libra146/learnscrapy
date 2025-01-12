import json
import re

import requests


def to_base_36(num):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if num == 0:
        return "0"
    result = ""
    while num > 0:
        num, remainder = divmod(num, 36)
        result = digits[remainder] + result
    return result


def ee(p, a, c, k, e, r):
    def e1(cc):
        result = ""
        if cc >= 62:
            result += e1(cc // 62)
        cc %= 62
        if cc > 35:
            result += chr(cc + 29)
        else:
            result += to_base_36(cc)
        return result

    c -= 1
    while c > 0:
        c -= 1
        r[e1(c)] = k[c]

    def temp_function(e: re.Match):
        return r.get(e.group(0), e.group(0))

    c = 1
    while c:
        c -= 1
        p = re.sub(r'\b[0-9a-zA-D]\b', temp_function, p)
    return p


res = requests.get('https://spa9.scrape.center/')
res.encoding = 'utf-8'

content, c, k = re.findall(r"\}\('(.*?)',\[],(\d\d),'(.*?),0,\{}\)", res.text)[0]
decode = ee(content, [], int(c), k[:-11].split('|'), 0, {})

print(decode.replace('\\', ''))

result = re.findall('players=(\[[\s\S]+\])', decode.replace('\\', ''))[0]  # type:str
json_content = json.loads(result.replace('\'', '"')
                          .replace('name', '"name"')
                          .replace('image', '"image"')
                          .replace('birthday', '"birthday"')
                          .replace('height', '"height"')
                          .replace('weight', '"weight"')
                          .replace('},]', '}]'))

for a in json_content:
    print(a)
