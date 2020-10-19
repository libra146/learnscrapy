# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

import pymysql


class LearnscrapyPipeline:
    def process_item(self, item, spider):
        return item


class SPA5Pipeline:
    def __init__(self):
        self.conn: pymysql.connect = None
        self.cur: pymysql.cursors.Cursor
        self.queue = []
        self.count = 0

    def open_spider(self, spider):
        self.conn = pymysql.connect(host='192.168.233.128', user='root', password='123456', db='test',
                                    port=3306, charset='utf8')
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        if len(self.queue) > 0:
            self.insert_database()
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.queue.append(
            (item['title'], item['author'], item['price'], item['time'], item['press'], item['page'], item['isbm']))
        if len(self.queue) > 300:
            s = time.time()
            self.insert_database()
            print(time.time() - s)
        return item

    def insert_database(self):
        sql = "insert into spa5 (title,author,price,time,press,page,isbm) values (%s,%s,%s,%s,%s,%s,%s)"
        self.cur.executemany(sql, self.queue)
        self.queue.clear()
        self.conn.commit()
