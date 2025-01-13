import json
import re

import requests


# 转成 36 进制
def to_base_36(num):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if num == 0:
        return "0"
    r = ""
    while num > 0:
        num, remainder = divmod(num, 36)
        r = digits[remainder] + r
    return r


# 原 js 的解码函数，稍微去掉了一些无用的逻辑
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

    return re.sub(r'\b[0-9a-zA-D]\b', lambda e: r.get(e.group(0), e.group(0)), p)


res = requests.get('https://spa9.scrape.center/')
res.encoding = 'utf-8'  # 不加可能会乱码

js_content, c, k = re.findall(r"\}\('(.*?)',\[],(\d\d),'(.*?),0,\{}\)", res.text)[0]
# 提取出来的 js 解码函数的参数，调用自己实现的解码函数
decode_content = ee(js_content, [], int(c), k[:-11].split('|'), 0, {})

print(decode_content.replace('\\', ''))

result = re.findall('players=(\[[\s\S]+\])', decode_content.replace('\\', ''))[0]  # type:str
json_content = json.loads(result.replace('\'', '"')
                          .replace('name', '"name"')
                          .replace('image', '"image"')
                          .replace('birthday', '"birthday"')
                          .replace('height', '"height"')
                          .replace('weight', '"weight"')
                          .replace('},]', '}]'))

for a in json_content:
    print(a)
