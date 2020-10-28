# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LearnscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Antispider6ScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    fraction = scrapy.Field()
    country = scrapy.Field()
    time = scrapy.Field()
    date = scrapy.Field()
    director = scrapy.Field()
