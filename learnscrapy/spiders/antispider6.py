import scrapy
from scrapy import Request
from scrapy.http import Response

from learnscrapy.items import Antispider6ScrapyItem


class Antispider6(scrapy.Spider):
    name = 'antispider6'
    # 建立cookie池
    cookies = []

    def start_requests(self):
        login_url = 'https://antispider6.scrape.center/login'
        for a in range(10):
            # 在循环中使用刚才注册的那几个账号登录,dont_filter参数用来防止不同的请求被过滤掉，URL去重默认是打开的
            yield scrapy.FormRequest(url=login_url, callback=self.add_cookie,
                                     formdata={'username': f'123456-{a}@qq.com', 'password': f'123456-{a}@qq.com'},
                                     dont_filter=True)

    def add_cookie(self, response: Response):
        # 将cookie保存起来
        self.cookies.append((response.request.headers.getlist('Cookie')))
        # 当全部账号都已经登录成功后即可开始爬取流程
        if len(self.cookies) >= 10:
            print('登录完成，开始爬取...')
            for a in range(1, 11):
                yield scrapy.Request(url=f'https://antispider6.scrape.center/page/{a}', callback=self.parse)

    def parse(self, response, **kwargs):
        result = response.xpath('//div[@class="el-card item m-t is-hover-shadow"]')
        for a in result:
            item = Antispider6ScrapyItem()
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
