import re

import scrapy
from scrapy import Request
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from learnscrapy.items import Antispider4ScrapyItem


class AntiSpider(scrapy.Spider):
    name = 'antispider4'
    css = {}

    def start_requests(self):
        urls = ['https://antispider4.scrape.center/css/app.654ba59e.css']
        for a in urls:
            # 解析css
            yield Request(url=a, callback=self.parse_css)

    def parse_css(self, response):
        # 根据规律使用正则找到所有需要用到的属性，由于这里只反爬了分数，所以只需要匹配少量的数字和点即可。
        result = re.findall(r'\.(icon-\d*?):before{content:"(.*?)"}', response.text)
        for key, value in result:
            self.css[key] = value
        print(self.css)
        # 访问主页
        yield SeleniumRequest(url='https://antispider4.scrape.center/', callback=self.parse_data,
                              wait_time=3, wait_until=EC.presence_of_element_located((By.CLASS_NAME, 'm-b-sm')))

    def parse_data(self, response):
        result = response.xpath('//div[@class="el-card item m-t is-hover-shadow"]')
        for a in result:
            item = Antispider4ScrapyItem()
            item['title'] = a.xpath('.//h2[@class="m-b-sm"]/text()').get()
            if r := a.xpath('.//p[@class="score m-t-md m-b-n-sm"]//i'):
                item['fraction'] = ''.join([self.css.get(b.xpath('.//@class').get()[5:], '') for b in r])
            item['country'] = a.xpath('.//div[@class="m-v-sm info"]/span[1]/text()').get()
            item['time'] = a.xpath('.//div[@class="m-v-sm info"]/span[3]/text()').get()
            item['date'] = a.xpath('.//div[@class="m-v-sm info"][2]/span/text()').get()
            url = a.xpath('.//a[@class="name"]/@href').get()
            print(response.urljoin(url))
            yield SeleniumRequest(url=response.urljoin(url), callback=self.parse, meta={'item': item},
                                  wait_time=3, wait_until=EC.presence_of_element_located((By.CLASS_NAME, 'm-b-sm')))

    def parse(self, response, **kwargs):
        item = response.meta['item']
        item['director'] = response.xpath(
            '//div[@class="directors el-row"]//p[@class="name text-center m-b-none m-t-xs"]/text()').get()
        yield item
