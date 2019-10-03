# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlQunarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    title = scrapy.Field()
    place = scrapy.Field()
    hot = scrapy.Field()
    level = scrapy.Field()
    site = scrapy.Field()
    note = scrapy.Field()
    price = scrapy.Field()
    sale = scrapy.Field()
