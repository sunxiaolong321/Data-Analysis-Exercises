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
        provinces = ['青海省']
        for province in provinces:
            print("正在爬取%s" % province)
            for page in [1,18,22,11]:
                print('正在爬取第%d页' % page)
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
