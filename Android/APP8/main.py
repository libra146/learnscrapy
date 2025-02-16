import base64
import hashlib
import time

import requests

page = 1
limit = 10


def encrypt(off):
    t = str(int(time.time()))
    l = ['/api/movie', '9fdLnciVh4FxQbri', str(off), t]
    sha1 = hashlib.sha1(','.join(l).encode()).hexdigest()
    return base64.b64encode(','.join([sha1, t]).encode()).decode()


url = 'https://app8.scrape.center/api/movie'

for a in range(10):
    data = {
        'offset': (page - 1) * limit,
        'limit': limit,
        'token': encrypt((page - 1) * limit)
    }
    print(data)
    r = requests.get(url, params=data).json()
    print(r)
    page += 1
    time.sleep(1)
