import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from learnscrapy.items import Antispider1ScrapyItem


class AntiSpider(scrapy.Spider):
    name = 'antispider1'

    def start_requests(self):
        urls = ['https://antispider1.scrape.center/']
        for a in urls:
            yield SeleniumRequest(url=a, callback=self.parse, wait_time=3, wait_until=EC.presence_of_element_located(
                (By.CLASS_NAME, 'm-b-sm')))

    def parse(self, response, **kwargs):
        result = response.xpath('//div[@class="el-card item m-t is-hover-shadow"]')
        for a in result:
            item = Antispider1ScrapyItem()
            item['title'] = a.xpath('.//h2[@class="m-b-sm"]/text()').get()
            item['fraction'] = a.xpath('.//p[@class="score m-t-md m-b-n-sm"]/text()').get().strip()
            item['country'] = a.xpath('.//div[@class="m-v-sm info"]/span[1]/text()').get()
            item['time'] = a.xpath('.//div[@class="m-v-sm info"]/span[3]/text()').get()
            item['date'] = a.xpath('.//div[@class="m-v-sm info"][2]/span/text()').get()
            url = a.xpath('.//a[@class="name"]/@href').get()
            print(response.urljoin(url))
            yield SeleniumRequest(url=response.urljoin(url), callback=self.parse_person, meta={'item': item},
                                  wait_time=3, wait_until=EC.presence_of_element_located((By.CLASS_NAME, 'm-b-sm')))

    def parse_person(self, response):
        item = response.meta['item']
        item['director'] = response.xpath(
            '//div[@class="directors el-row"]//p[@class="name text-center m-b-none m-t-xs"]/text()').get()
        yield item
