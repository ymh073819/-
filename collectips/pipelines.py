# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class CollectipsPipeline(object):
    def process_item(self, item, spider):
        return item


class TutorialPipeline(object):
    Insert = '''insert into proxy_ip(ip,port,address,annoy,type,live,check_time)
                        values('{ip}','{port}','{address}','{annoy}','{type}','{live}','{check}')'''

    def __init__(self, settings):
        self.settings = settings

    def process_item(self, item, spider):
        print(item)
        if spider.name == "xici":
            sqltext = self.Insert.format(
                ip=pymysql.escape_string(item['ip']),
                port=pymysql.escape_string(item['port']),
                address=pymysql.escape_string(item['address']),
                annoy=pymysql.escape_string(item['annoy']),
                type=pymysql.escape_string(item['type']),
                live=pymysql.escape_string(item['live']),
                check=pymysql.escape_string(item['check']))
            # spider.log(sqltext)
            self.cursor.execute(sqltext)

        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
