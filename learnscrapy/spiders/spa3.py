import scrapy
from scrapy import Request

from learnscrapy.items import SPA3Item


class SPA3Spider(scrapy.Spider):
    name = "spa3"
    offset = 0
    url = 'https://spa3.scrape.center/api/movie/?limit=10&offset=%s'

    def start_requests(self):
        urls = [self.url % self.offset]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        result = response.json()
        for a in result['results']:
            item = SPA3Item()
            item['title'] = a['name'] + a['alias']
            item['fraction'] = a['score']
            item['country'] = '、'.join(a['regions'])
            item['time'] = a['minute']
            item['date'] = a['published_at']
            yield Request(url=response.urljoin(f'/api/movie/{a["id"]}/'), callback=self.parse_person,
                          meta={'item': item})
        if self.offset < result['count']:
            # 因为每次请求限制10条数据，所以每次将偏移量+10
            self.offset += 10
            yield Request(url=self.url % self.offset, callback=self.parse)

    def parse_person(self, response):
        result = response.json()
        item = response.meta['item']
        item['director'] = result['directors'][0]['name']
        yield item
