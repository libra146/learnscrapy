import time

import pywasm
import requests
import urllib3

pywasm.log.lvl = 1
urllib3.disable_warnings()
runtime = pywasm.core.Runtime()
m = runtime.instance_from_file('Wasm.wasm')


def get_sign(offset, t):
    r = runtime.invocate(m, 'encrypt', [offset, t])
    print(f'fib(10) = {r[0]}')
    return r[0]


def get_content():
    for offset in range(0, 110):
        sign = get_sign(offset, int(time.time()))
        url = f'https://spa14.scrape.center/api/movie/?limit=10&offset={offset}&sign={sign}'
        r = requests.get(url, verify=False).json()
        print(r)


if __name__ == '__main__':
    get_content()
