import time

import requests

page = 1
limit = 10

url = 'https://app9.scrape.center/api/movie'

for a in range(10):
    data = {
        'offset': (page - 1) * limit,
        'limit': limit,
        'token': 'YjhjODBlMDQyNWVkYjk4NmQyMzQ2MWM2NWE0NzlkODY4YmMwZjczZSwxNzM5ODAxODU0'
    }
    print(data)
    r = requests.get(url, params=data).json()
    print(r)
    page += 1
    time.sleep(1)
