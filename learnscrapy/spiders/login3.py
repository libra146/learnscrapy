import scrapy
from scrapy import Request

from learnscrapy.items import Login3ScrapyItem


class Login3(scrapy.Spider):
    name = 'login3'
    jwt = ''
    offset = 0
    limit = 18
    url = f'https://login3.scrape.center/api/book/?limit={limit}&offset=%s'

    def start_requests(self):
        # 添加需要提交的表单参数
        yield scrapy.FormRequest(url='https://login3.scrape.center/api/login', callback=self.parse,
                                 formdata={'username': 'admin', 'password': 'admin'})

    def parse(self, response, **kwargs):
        result = response.json()
        # 从响应中获取到 jwt
        if 'token' in result:
            self.jwt = result['token']
        # 从起始页面开始爬取
        yield scrapy.Request(url=self.url % self.offset, callback=self.parse_page)

    def parse_page(self, response, **kwargs):
        result = response.json()
        print(response.url)
        for a in result['results']:
            item = Login3ScrapyItem()
            item['title'] = a['name']
            item['author'] = '/'.join([c.strip() for c in (a['authors'] or [])])
            yield Request(url=f'https://login3.scrape.center/api/book/{a["id"]}/', callback=self.parse3,
                          meta={'item': item})
        if int(result['count']) > self.offset:
            self.offset += self.limit
            yield Request(url=self.url % self.offset, callback=self.parse_page)

    def parse3(self, response):
        item = response.meta['item']
        result = response.json()
        item['price'] = result['price'] or 0
        item['time'] = result['published_at']
        item['press'] = result['publisher']
        item['page'] = result['page_number']
        item['isbm'] = result['isbn']
        yield item
