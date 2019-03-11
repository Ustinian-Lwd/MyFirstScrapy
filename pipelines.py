# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class MyfirstscrapyPipeline(object):
#     def process_item(self, item, spider):
#         return item


from scrapy.exceptions import DropItem
import pymongo

# 处理要存储的数据
# item['text']
class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item["text"]) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem("Missing Text")


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB")
        )

    # 开启爬虫的时候初始化操作
    def open_spider(self, spider):
        # 连接mongodb
        self.client = pymongo.MongoClient(self.mongo_uri)
        # 相当于mysql的游标
        # 找到数据库
        self.db = self.client[self.mongo_db]

    #
    def process_item(self, item, spider):
        name = item.__class__.__name__
        print("李旺东：", name)
        # print("item['text']==", item["text"])
        # print("item['author']==", item["author"])
        # print("item['tags']==", item["tags"])
        self.db[name].insert(dict(item))
        return item

    # 关闭爬虫
    def close_spider(self, spider):
        self.client.close()
