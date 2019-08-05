# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BossdirecruitspiderPipeline(object):
    def process_item(self, item, spider):
        print('工作名称：', item['job_name'])
        print('薪资待遇：', item['job_salary'])
        print('工作地点：', item['job_place'])
        print('学历要求：', item['job_edu'])
        print('工作经验：', item['job_experience'])
        print('公司名称：', item['company_name'])
        print('招聘信息链接：', item['job_detail'])
        print('行业类型：', item['industry'])
        print('融资类型：', item['financing'])
        print('公司规模：', item['company_population'])
        print('招聘者：', item['recruiter'])
        print('招聘者职业身份：', item['recruiter_id'])
        return item
