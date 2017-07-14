# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from jobboleSpider.items import JoBoleArticleItem
from jobboleSpider.utils.common import get_md5
import datetime
from scrapy.loader import ItemLoader
from urllib import parse

class ArticleSpider(scrapy.Spider):
    name = "Article"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1.获取文章列表也中具体文章url,并交给scrapy进行下载后并进行解析
        2.获取下一页的url并交给scrapy进行下载，下载完成后，交给parse
        :param response:
        :return:
        '''
        #解析列表页中所有文章的url，并交给scrapy下载后进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            #image_url是图片的地址
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            #这里通过meta参数将图片的url传递进来，这里用parse.urljoin的好处是如果有域名我前面的response.url不生效
            # 如果没有就会把response.url和post_url做拼接
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":parse.urljoin(response.url,image_url)},callback=self.parse_detail)

        #提取下一页并交给scrapy下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=next_url,callback=self.parse)

    def parse_detail(self,response):
        '''
        获取文章的详细内容
        :param response:
        :return:
        '''
        article_item = JoBoleArticleItem()



        front_image_url = response.meta.get("front_image_url","")  #文章封面图地址
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()


        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().split()[0]

        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tag =",".join(tag_list)
        praise_nums = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()
        if len(praise_nums) == 0:
            praise_nums = 0
        else:
            praise_nums = int(praise_nums[0])
        fav_nums  = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        match_re = re.match(".*(\d+).*",fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        comment_nums =response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_com = re.match(".*(\d+).*",comment_nums)
        if match_com:
            comment_nums = int(match_com.group(1))
        else:
            comment_nums=0

        content = response.xpath('//div[@class="entry"]').extract()[0]


        article_item["url_object_id"] = get_md5(response.url) #这里对地址进行了md5变成定长
        article_item["title"] = title
        article_item["url"] = response.url
        try:
            create_date = datetime.datetime.strptime(create_date,'%Y/%m/%d').date()
        except Exception as e:
            create_date = datetime.datetime.now().date()

        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = int(praise_nums)
        article_item["fav_nums"] = fav_nums
        article_item["comment_nums"] = comment_nums
        article_item["tag"] = tag
        article_item['content'] = content

        yield article_item


















