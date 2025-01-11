# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql


class LearnscrapyPipeline:
    def process_item(self, item, spider):
        return item


class SPA2Pipeline:
    def __init__(self):
        self.conn: pymysql.connect = None
        self.cur: pymysql.cursors.Cursor
        self.queue = []
        self.count = 0

    def open_spider(self, spider):
        self.conn = pymysql.connect(host='172.24.233.27', user='root', password='123456', db='test',
                                    port=60101, charset='utf8')
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        if len(self.queue) > 0:
            self.insert_database()
        self.cur.close()
        self.conn.close()

    def insert_database(self):
        sql = "insert into ssr1 (country,date,director,fraction,time,title) values (%s,%s,%s,%s,%s,%s)"
        self.cur.executemany(sql, self.queue)
        self.queue.clear()
        self.conn.commit()

    def process_item(self, item, spider):
        self.queue.append(
            (item['country'], item['date'], item['director'], item['fraction'], item['time'], item['title']))
        if len(self.queue) > 30:
            self.insert_database()
        return item
