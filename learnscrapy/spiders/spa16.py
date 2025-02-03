import scrapy


class DemoSpider(scrapy.Spider):
    name = "spa16"
    allowed_domains = ["spa16.scrape.center"]
    start_urls = ["https://spa16.scrape.center/api/book/?limit=18&offset=0"]

    def parse(self, response, **kwargs):
        print(response.body.decode('utf-8'))
