# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TrainqueryspiderItem(scrapy.Item):
    #   1车次
    train_number = scrapy.Field()
    #   2出发站
    departure_station = scrapy.Field()
    #   3到达站
    arrival_station = scrapy.Field()
    #   4出发时间
    departure_time = scrapy.Field()
    #   5到达时间
    arrival_time = scrapy.Field()
    #   6历时
    need_time = scrapy.Field()
    #   7商务座/特等座
    business_class = scrapy.Field()
    #  8一等座
    first_class = scrapy.Field()
    #   9二等座
    second_class = scrapy.Field()
    #   10高级软卧
    private_soft = scrapy.Field()
    #   11软卧/一等卧
    first_soft = scrapy.Field()
    #   12动卧
    pssive_seat = scrapy.Field()
    #   13硬卧/二等卧
    second_soft = scrapy.Field()
    #   14软座
    soft_seat = scrapy.Field()
    #   15硬座
    hard_seat = scrapy.Field()
    #   16备注（是否可预订）
    reservation = scrapy.Field()
    #  17无座
    without_seat = scrapy.Field()
    #   18其他
    other = scrapy.Field()



