import scrapy
from scrapy import Request

from learnscrapy.items import SPA4Item


class SPA4Spider(scrapy.Spider):
    name = "spa4"
    offset = 0
    limit = 100
    url = f'https://spa4.scrape.center/api/news/?limit={limit}&offset=%s'

    def start_requests(self):
        urls = [self.url % self.offset]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        result = response.json()
        print(response.url)
        for a in result['results']:
            item = SPA4Item()
            item['code'] = a['code']
            item['published_at'] = a['published_at']
            item['title'] = a['title']
            item['updated_at'] = a['updated_at']
            item['url'] = a['url']
            item['website'] = a['website']
            # 新闻网址都是外部链接，抓取方式都不一样，就不抓取具体信息了
            yield item
        if int(result['count']) > self.offset:
            self.offset += self.limit
            yield Request(url=self.url % self.offset, callback=self.parse)
