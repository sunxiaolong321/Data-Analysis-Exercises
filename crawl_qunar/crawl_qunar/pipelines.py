# -*- coding: utf-8 -*-
# Define your item pipelines here
from twisted.enterprise import adbapi
import pymysql
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 同步爬取


class MysqlPipeline(object):
    def __init__(self):
        # 链接本地数据库
        self.conn = pymysql.connect(host='127.0.0.1', port=3306,
                                    user='root', password=', database='qunar',
                                    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        item = dict(item)
        cols = ", ".join('`{}`'.format(k) for k in item.keys())
        val_cols = ", ".join('%({})s'.format(k) for k in item.keys())
        insert_sql = "insert into message(%s) VALUES(%s)" % (cols, val_cols)
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, item)
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host="127.0.0.1",
            db='qunar',
            user='root',
            passwd='380324',
            port=3306,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )

        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将mysql插入变成异步执行，采用异步的机制写入mysql
        :param item:
        :param spider:
        :return:
        """
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):

        item = dict(item)
        cols = ", ".join('`{}`'.format(k) for k in item.keys())
        val_cols = ", ".join('%({})s'.format(k) for k in item.keys())
        insert_sql = "insert into message(%s) VALUES(%s)" % (cols, val_cols)
        # 执行插入数据到数据库操作
        cursor.execute(insert_sql, item)