# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import json
import codecs
import pymysql
from twisted.enterprise import adbapi


class JobbolespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    '''
    返回json数据到文件
    '''
    def __init__(self):
        self.file = codecs.open("article.json",'w',encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self,spider):
        self.file.close()


class MysqlPipeline(object):
    '''
    插入mysql数据库
    '''
    def __init__(self):
        self.conn =pymysql.connect(host='192.168.1.19',port=3306,user='root',passwd='123456',db='article_spider',use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql = '''
        insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,front_image_path,comment_nums,fav_nums,praise_nums,tag,content) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''

        self.cursor.execute(insert_sql,(item["title"],item["create_date"],item["url"],item["url_object_id"],item["front_image_url"],item["front_image_path"],item["comment_nums"],item["fav_nums"],item["praise_nums"],item["tag"],item["content"]))
        self.conn.commit()


class MysqlTwistedPipline(object):
    '''
    采用异步的方式插入数据
    '''
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            port = settings["MYSQL_PORT"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWD"],
            db = settings["MYSQL_DB"],
            use_unicode = True,
            charset="utf8",
        )
        dbpool = adbapi.ConnectionPool("pymysql",**dbparms)
        return cls(dbpool)
    def process_item(self,item,spider):
        '''
        使用twisted将mysql插入变成异步
        :param item:
        :param spider:
        :return:
        '''
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)

    def handle_error(self,failure):
        #处理异步插入的异常
        print(failure)

    def do_insert(self,cursor,item):
        #具体插入数据
        insert_sql = '''
        insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,front_image_path,comment_nums,fav_nums,praise_nums,tag,content) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        cursor.execute(insert_sql,(item["title"],item["create_date"],item["url"],item["url_object_id"],item["front_image_url"],item["front_image_path"],item["comment_nums"],item["fav_nums"],item["praise_nums"],item["tag"],item["content"]))



class ArticleImagePipeline(ImagesPipeline):
    '''
    对图片的处理
    '''
    def item_completed(self, results, item, info):

        for ok ,value in results:
            if ok:
                image_file_path = value["path"]
                item['front_image_path'] = image_file_path
            else:
                item['front_image_path'] = ""


        return item
