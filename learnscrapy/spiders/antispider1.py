import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class AntiSpider(scrapy.Spider):
    name = 'antispider1'

    def start_requests(self):
        urls = ['https://antispider4.scrape.center/']
        for a in urls:
            yield SeleniumRequest(url=a, callback=self.parse, wait_time=3, wait_until=EC.presence_of_element_located(
                (By.CLASS_NAME, 'm-b-sm')))

    def parse(self, response, **kwargs):
        print(response.text)
        input()
