# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import time

import pymongo as pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import CloseSpider


class LearnscrapyPipeline:
    def process_item(self, item, spider):
        return item


class Antispider7Pipeline:
    def __init__(self):
        self.client: pymongo.MongoClient
        self.queue = []
        self.count = 0

    def open_spider(self, spider):
        # 从环境变量中提取数据库url
        if url := os.getenv('MONGOTEST'):
            pass
        else:
            raise CloseSpider('mongo url is null!')
        self.client = pymongo.MongoClient(url)
        self.db = self.client['test']

    def close_spider(self, spider):
        if len(self.queue) > 0:
            self.insert_database()
        self.client.close()

    def insert_database(self):
        start = time.time()
        self.db['test'].insert_many(self.queue)
        print(time.time() - start)
        self.queue.clear()

    def process_item(self, item, spider):
        self.queue.append(ItemAdapter(item).asdict())
        if len(self.queue) > 10:
            self.insert_database()
        return item
