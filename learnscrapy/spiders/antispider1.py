import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from learnscrapy.items import Antispider3ScrapyItem


class AntiSpider(scrapy.Spider):
    name = 'antispider3'

    def start_requests(self):
        urls = ['https://antispider3.scrape.center/']
        for a in urls:
            yield SeleniumRequest(url=a, callback=self.parse, wait_time=3, wait_until=EC.presence_of_element_located(
                (By.CLASS_NAME, 'm-b-sm')))

    def parse(self, response, **kwargs):
        result = response.xpath('//div[@class="el-card__body"]')
        for a in result:
            item = Antispider3ScrapyItem()
            chars = {}
            # 有反爬
            if r := a.xpath('.//h3[@class="m-b-sm name"]//span'):
                for b in r:
                    chars[b.xpath('.//@style').re(r'\d\d?')[0]] = b.xpath('.//text()').get().strip()
                # 先用sorted函数来排序，使用lambda指定索引值为0的值，也就是根据key值来排序，排序后使用zip函数来将所有的字符串放到
                # 同一个元组中，list函数用来将生成器转成列表，之后使用索引值选择title所在的元组，使用join函数连接所有的字符串即为标题字符串
                item['title'] = ''.join(list(zip(*sorted(chars.items(), key=lambda i: i[0])))[1])
            else:
                # 没有反爬
                item['title'] = a.xpath('.//h3[@class="name whole"]/text()').get()
            item['author'] = a.xpath('.//p[@class="authors"]/text()').get().strip()
            url = a.xpath('.//a/@href').get()
            print(response.urljoin(url))
            yield SeleniumRequest(url=response.urljoin(url), callback=self.parse_person, meta={'item': item},
                                  wait_time=3, wait_until=EC.presence_of_element_located((By.CLASS_NAME, 'm-b-sm')))

    def parse_person(self, response):
        item = response.meta['item']
        item['price'] = response.xpath('//p[@class="price"]/span/text()').get()
        item['time'] = response.xpath('//p[@class="published-at"]/text()').get()
        item['press'] = response.xpath('//p[@class="publisher"]/text()').get()
        item['page'] = response.xpath('//p[@class="page-number"]/text()').get()
        item['isbm'] = response.xpath('//p[@class="isbn"]/text()').get()
        yield item
