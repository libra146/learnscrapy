# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

import pymongo as pymongo
from itemadapter import ItemAdapter


class LearnscrapyPipeline:
    def process_item(self, item, spider):
        return item


class Login2Pipeline:
    def __init__(self):
        self.client: pymongo.MongoClient
        self.queue = []
        self.count = 0

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='172.24.233.27', port=60103, username='root', password='123456')
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
        if len(self.queue) > 50:
            self.insert_database()
        return item
