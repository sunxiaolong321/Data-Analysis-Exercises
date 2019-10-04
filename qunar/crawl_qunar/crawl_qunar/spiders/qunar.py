# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import CrawlQunarItem
from urllib.parse import urlencode
import json

COUNT = 0


class QunarSpider(scrapy.Spider):
    name = 'qunar'
    allowed_domains = ['qunar.com']
    # start_urls = ['https://piao.qunar.com/']

    def start_requests(self):
        # 构造关键词
        provinces = ["北京市","天津市","上海市","重庆市","河北省","山西省","辽宁省","吉林省",\
            "黑龙江省","江苏省","浙江省","安徽省","福建省","江西省","山东省","河南省","湖北省",\
                "湖南省","广东省","海南省","四川省","贵州省","云南省","陕西省","甘肃省","青海省",\
                    "台湾省","内蒙古自治区","广西壮族自治区","西藏自治区","宁夏回族自治区",\
                        "新疆维吾尔自治区","香港特别行政区","澳门特别行政区"]
        for province in provinces:
            print("正在爬取%s" % province)
            for page in range(1,31):
                url = "https://piao.qunar.com/ticket/list.htm?keyword=%s&page=%s" % (
                    province, page)
                try:
                    yield Request(url, self.parse, meta={'keyword': province})
                except:
                    break

    def parse(self, response):
        contenter = response.xpath('//*[@id="search-list"]/div/div/div[2]')
        for item in contenter:
            global COUNT
            COUNT += 1
            print("\r正在解析第%d条信息"%COUNT,end='')
            qunar = CrawlQunarItem()
            qunar['title'] = item.xpath('./h3/a/text()').extract_first()
            qunar['place'] = item.xpath(
                './div/div[1]/span/a/text()').extract_first()
            try:
                qunar['hot'] = float(item.xpath(
                    './div/div[1]/div/span[1]/em/span/text()').extract_first()[3:])
            except:
                qunar['hot'] = 0.0
            level = item.xpath(
                './div/div[1]/span[1]/text()').extract_first()
            if level == "[":
                level = None
            qunar['level'] = level
            qunar['site'] = item.xpath('./div/p/span/text()').extract_first()
            qunar['note'] = item.xpath('./div/div[2]/text()').extract_first()
            qunar['city'] = response.meta['keyword']
            try:
                qunar['price'] = float(item.xpath(
                    './following-sibling::div[1]/table/tr[1]/td/span/em/text()').extract_first())
            except:
                qunar['price'] = 0.0
            try:
                qunar['sale'] = int(item.xpath(
                    './following-sibling::div[1]/table/tr[4]/td/span/text()').extract_first())
            except:
                qunar['sale'] = 0
            yield qunar
