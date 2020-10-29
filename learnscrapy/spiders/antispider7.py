import scrapy
from scrapy import Request
from scrapy.http.request.json_request import JsonRequest

from learnscrapy.items import Antispider7ScrapyItem


class Antispider7(scrapy.Spider):
    name = 'antispider7'
    # 建立cookie池
    cookies = []
    offset = 0
    limit = 18
    url = f'https://antispider7.scrape.center/api/book/?limit={limit}&offset=%s'

    def start_requests(self):
        login_url = 'https://antispider7.scrape.center/api/login'
        # login_url = 'http://httpbin.org'
        for a in range(10):
            # 使用json格式登录，不使用表单
            yield JsonRequest(url=login_url, callback=self.add_cookie, method='POST',
                              data={'username': f'12345678{a}', 'password': f'12345678{a}'},
                              dont_filter=True)

    def add_cookie(self, response):
        # 将cookie保存起来
        self.cookies.append(response.json()['token'])
        # 当全部账号都已经登录成功后即可开始爬取流程
        if len(self.cookies) >= 10:
            print('登录完成，开始爬取...')
            urls = [self.url % self.offset]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                     meta={'change_proxy': 0, 'change_cookie': 0})

    def parse(self, response, **kwargs):
        result = response.json()
        print(response.url)
        for a in result['results']:
            item = Antispider7ScrapyItem()
            item['title'] = a['name']
            item['author'] = '/'.join(a['authors'] or [])
            yield Request(url=f'https://antispider7.scrape.center/api/book/{a["id"]}/', callback=self.parse2,
                          meta={'item': item, 'change_proxy': 0, 'change_cookie': 0})
        # 原始数据量太大了，这里只爬取200条
        if 200 > self.offset:
            self.offset += self.limit
            yield Request(url=self.url % self.offset, callback=self.parse)

    def parse2(self, response):
        item = response.meta['item']
        result = response.json()
        item['price'] = result['price'] or 0
        item['time'] = result['published_at']
        item['press'] = result['publisher']
        item['page'] = result['page_number']
        item['isbm'] = result['isbn']
        yield item
