# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaidashoppingspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 商品类型
    good_type = scrapy.Field()
    # 商品图片
    good_picture = scrapy.Field()
    # 商品名称属性
    good_alt = scrapy.Field()
    # 商品价格
    good_price = scrapy.Field()
    # 配送店家
    hotel = scrapy.Field()
    # 商品详情链接
    good_detail_url = scrapy.Field()
