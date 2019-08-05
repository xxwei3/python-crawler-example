# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossdirecruitspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 工作名称
    job_name = scrapy.Field()
    # 薪资待遇
    job_salary = scrapy.Field()
    # 工作地点
    job_place = scrapy.Field()
    # 学历要求
    job_edu = scrapy.Field()
    # 工作年限
    job_experience = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 招聘详情链接
    job_detail = scrapy.Field()
    # 行业类型
    industry = scrapy.Field()
    # 融资类型
    financing = scrapy.Field()
    # 公司规模
    company_population = scrapy.Field()
    # 招聘者
    recruiter = scrapy.Field()
    # 招聘者职业身份
    recruiter_id = scrapy.Field()


    # pass
