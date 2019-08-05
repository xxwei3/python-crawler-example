# -*- coding: utf-8 -*-
import scrapy

from BossDirecruitSpider.items import BossdirecruitspiderItem

# 第一个爬虫练习案例
class JobInfoSpider(scrapy.Spider):
    name = 'job_info'
    allowed_domains = ['zhipin.com']
    # 合肥地区的java岗位招聘信息
    # start_urls = ['https://www.zhipin.com/c101220100-p100101/']
    # 合肥地区web前端招聘信息
    start_urls = ['https://www.zhipin.com/job_detail/?query=&city=101220100&industry=&position=']
    # 合肥地区人事行政前台招聘信息
    # start_urls = ['https://www.zhipin.com/c101220100-p150202/?ka=search_150202']
    # 合肥地区汽车行业4S店管理岗位招聘信息
    # start_urls = ['https://www.zhipin.com/c101220100-p230208/?ka=search_230208']

    def parse(self, response):
        # 公共xpath路径
        public_node = response.xpath('//div[@class="job-primary"]')
        for node in public_node:
            item = BossdirecruitspiderItem()

            # info-primary的工作信息：名称，薪资，地点，学历，工作经验
            item['job_name'] = node.xpath('.//div[@class="job-title"]/text()').extract_first()
            item['job_salary'] = node.xpath('.//div[@class="info-primary"]/h3/a/span/text()').extract_first()
            # 该节点包含（地点，学历，工作经验），需要用extract()获取列表
            work_infos = node.xpath('.//div[@class="info-primary"]/p/text()').extract()
            if work_infos and len(work_infos) > 2:
                item['job_place'] = work_infos[0]
                item['job_edu'] = work_infos[1]
                item['job_experience'] = work_infos[2]
            if work_infos and len(work_infos) <= 1:
                item['job_place'] = work_infos[0]
                item['job_edu'] = ""
                item['job_experience'] = ""

            # info-company的公司信息：公司名称、招聘详情链接、行业类型、融资类型、公司规模
            item['company_name'] = node.xpath('.//div[@class="info-company"]/div/h3/a/text()').extract_first()
            # 招聘详情链接，需要拼接前缀“www.zhipin.com”
            prefix_url = 'https://www.zhipin.com'
            item['job_detail'] = prefix_url + node.xpath('.//div[@class="info-company"]/div/h3/a/@href').extract_first()
            # 该节点包含（行业类型、融资类型、公司规模），需要用extract()获取列表
            company_infos = node.xpath('.//div[@class="info-company"]/div/p/text()').extract()
            if company_infos and len(company_infos) > 2:
                item['industry'] = company_infos[0]
                item['financing'] = company_infos[1]
                item['company_population'] = company_infos[2]
            if company_infos and len(company_infos) <= 2:
                item['industry'] = company_infos[0]
                item['financing'] = ""
                item['company_population'] = company_infos[1]

            # info-publis的招聘者信息：招聘者姓名，职业身份
            publis_infos = node.xpath('.//div[@class="info-publis"]/h3/text()').extract()
            if publis_infos and len(publis_infos) > 1:
                item['recruiter'] = publis_infos[0]
                item['recruiter_id'] = publis_infos[1]
            if publis_infos and len(publis_infos) <= 1:
                item['recruiter'] = publis_infos[0]
                item['recruiter_id'] = ""

            # yield 将会创建一个生成器,将 item 对象返回给 Scrapy 引擎
            yield item

            # 定义下页标签的元素位置
            # next_page = response.xpath('//div[@class="page"]/a/@href').extract()[4]
            next_page = response.xpath('//div[@class="page"]/a/@href').extract()[-1]
            # 判断是否到了最后一页
            if next_page != 'javascript:;':
                url = prefix_url + next_page
                yield scrapy.Request(url=url, callback=self.parse)
