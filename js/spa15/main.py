import ctypes
import time

import requests
import urllib3

urllib3.disable_warnings()
dll = ctypes.CDLL('./c99/wasm.so')
dll.init_wasm()  # 别忘了初始化


def encrypt(p1, p2):
    print(p1, p2)
    dll.encrypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    dll.encrypt.restype = ctypes.c_char_p
    a1 = ctypes.c_char_p(p1.encode('utf-8'))
    a2 = ctypes.c_char_p(p2.encode('utf-8'))
    result = dll.encrypt(a1, a2)
    return result.decode()


def get_content():
    for offset in range(0, 110):
        sign = encrypt('/api/movie', str(int(time.time())))
        url = f'https://spa15.scrape.center/api/movie/?limit=10&offset={offset}&token={sign}'
        r = requests.get(url, verify=False).text
        print(r)
        time.sleep(0.5)


if __name__ == '__main__':
    # print(encrypt('/api/movie', '1738565280'))
    get_content()
