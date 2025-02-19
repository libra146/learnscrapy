import time

import requests

page = 1
limit = 10

url = 'https://app9.scrape.center/api/movie'

for a in range(10):
    data = {
        'offset': (page - 1) * limit,
        'limit': limit,
        'token': requests.post('http://127.0.0.1:9999/api/app9/do-work',
                               json={'str1': '/api/movie', 'int1': (page - 1) * limit}).text
    }
    print(data)
    r = requests.get(url, params=data).json()
    print(r)
    page += 1
    time.sleep(1)
