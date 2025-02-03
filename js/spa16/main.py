import time

import httpx


def httpx_():
    client = httpx.Client(http2=True)
    for a in range(0, 110, 10):
        res = client.get(f'https://spa16.scrape.center/api/book/?limit=18&offset={a}')
        print(res.json())
        time.sleep(1)


if __name__ == '__main__':
    httpx_()
