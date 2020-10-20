import base64
import json

import requests

if __name__ == '__main__':
    # execute(['scrapy', 'crawl', 'spa1'])

    data = {
        'username': 'admin',
        'password': 'admin'
    }
    url = 'https://login1.scrape.center/'
    # 注意这里是 get 请求，如果是 post 请求的话会报405错误代码。
    r = requests.get(url=url, data={'token': base64.b64encode(json.dumps(data).encode())})
    print(r.text)
    print(r.status_code)
