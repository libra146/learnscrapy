# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

import pymongo
from itemadapter import ItemAdapter


class LearnscrapyPipeline:
    def process_item(self, item, spider):
        return item


class Antispider3Pipeline:
    def __init__(self):
        self.client: pymongo.MongoClient
        self.queue = []
        self.count = 0

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='192.168.233.128', port=27017)
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
        result = ItemAdapter(item).asdict()
        # 处理掉多余的空格
        for key, value in result.items():
            if result[key]:
                result[key] = value.strip()
        self.queue.append(result)
        if len(self.queue) > 50:
            self.insert_database()
        return item
