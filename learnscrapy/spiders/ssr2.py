import scrapy
from scrapy import Request

from learnscrapy.items import SSR2Item


class SSR2Spider(scrapy.Spider):
    name = "ssr2"

    def start_requests(self):
        urls = [
            f'http://ssr2.scrape.center/page/{a}' for a in range(1, 11)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        result = response.xpath('//div[@class="el-card item m-t is-hover-shadow"]')
        for a in result:
            item = SSR2Item()
            item['title'] = a.xpath('.//h2[@class="m-b-sm"]/text()').get()
            item['fraction'] = a.xpath('.//p[@class="score m-t-md m-b-n-sm"]/text()').get().strip()
            item['country'] = a.xpath('.//div[@class="m-v-sm info"]/span[1]/text()').get()
            item['time'] = a.xpath('.//div[@class="m-v-sm info"]/span[3]/text()').get()
            item['date'] = a.xpath('.//div[@class="m-v-sm info"][2]/span/text()').get()
            url = a.xpath('.//a[@class="name"]/@href').get()
            yield Request(url=response.urljoin(url), callback=self.parse_person, meta={'item': item})

    def parse_person(self, response):
        item = response.meta['item']
        item['director'] = response.xpath(
            '//div[@class="directors el-row"]//p[@class="name text-center m-b-none m-t-xs"]/text()').get()
        yield item
