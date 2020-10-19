# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LearnscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SPA4Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    published_at = scrapy.Field()
    title = scrapy.Field()
    updated_at = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()
