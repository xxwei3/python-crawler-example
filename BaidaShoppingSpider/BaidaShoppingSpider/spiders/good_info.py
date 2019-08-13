# -*- coding: utf-8 -*-
import scrapy
from BaidaShoppingSpider.items import BaidashoppingspiderItem
import good_dict_setting
import good_input_tip


class GoodInfoSpider(scrapy.Spider):
    name = 'good_info'
    allowed_domains = ['bdego.com']
    # 按提示查询需要的商品分类信息
    good_type = good_input_tip.input_tip()
    # cid
    cid_list = good_dict_setting.good_type_dicts.get(good_type)
    cid_code = cid_list[0]
    cid_name = cid_list[1].decode('utf-8')
    # print (u'当前类别的code---->', cid_code)
    # print (u'当前类别的name---->', cid_name)
    # 拼接url
    start_url = 'http://www.bdego.com/product_list.jsp?cid=c_{}&keyword='.format(cid_code)

    start_urls = [start_url]

    def __init__(self):
        self._current_page_int = 1
        self._cid_code = GoodInfoSpider.cid_code
        self._cid_name = GoodInfoSpider.cid_name

    def parse(self, response):
        public_path = response.xpath('//*[@id="prodcutListUl"]//li')
        base_url = 'http://www.bdego.com'
        for node in public_path:
            item = BaidashoppingspiderItem()
            # 商品类型
            item['good_type'] = self._cid_name
            # 商品图片
            item['good_picture'] = node.xpath('.//div[@class="pic"]/div/a/img/@src').extract()[0]
            # 商品名称属性
            item['good_alt'] = node.xpath('.//div[@class="txt"]/a/text()').extract()[0]
            # 配送店家
            item['hotel'] = node.xpath('.//div[@class="price"]/span/a/text()').extract()[0]
            # 商品详情链接
            item['good_detail_url'] = base_url + node.xpath('.//div[@class="pic"]/div/a/@href').extract()[0]
            # 商品价格，数据中含有回车和空格键，需要处理一下
            price = node.xpath('.//div[@class="price"]/text()').extract()[1]
            price = price.replace(u'\r\n                                        \xa5', u'￥')
            item['good_price'] = price

            yield item

        # 爬取所有页，判断下一页是否是到了最后一页
        page_node = response.xpath('//*[@id="infoPage"]/ul//li')
        # 监测下一页按钮的变化
        next_page_tip = page_node.xpath('./a[@class="downPage"]/@title').extract_first()
        # 找到当前的页码
        current_page = page_node.xpath('./a[@class="nowPage"]/text()').extract_first()
        # str转成整型
        self._current_page_int = int(current_page) + 1

        print (u'是否为最后一页------>', next_page_tip)
        # 将unicede转为str进行比较
        if next_page_tip.encode('utf-8') != '目前已是最后一页':
            page_url = 'http://www.bdego.com/list-{}/p{}.html'.format(self._cid_code, self._current_page_int)
            print (u'当前页码------>', current_page)
            print (u'当前utl------>', page_url)
            yield scrapy.Request(url=page_url, callback=self.parse)
