# -*- coding: utf-8 -*-
import scrapy
import station_info
import stations
import messy_code
import custom_search
import json
import os

from TrainQuerySpider.items import TrainqueryspiderItem


class QueryInfoSpider(scrapy.Spider):
    # 一、将Python的默认编码方式修改为utf-8
    messy_code.code_utf8()

    # 二、初始化站点信息的js请求，并保存本地stations.txt中，将格式改为stations.py即可使用
    paths = os.getcwd() + '\\12306'
    if not os.path.exists(paths):
        print (u'----OK--------初始化站点信息的js请求并保存到本地备用-------------')
        station_info.save_station(paths)

    # 三、用户输入查询条件进行自定义查询
    start_url = custom_search.query_custom()

    name = 'query_info'
    allowed_domains = ['kyfw.12306.cn']
    start_urls = [start_url]

    # 合肥--阜阳  8.8号
    # start_urls = [
    #     'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2019-08-08&leftTicketDTO.from_station=HFH&leftTicketDTO.to_station=FYH&purpose_codes=ADULT']

    # 合肥--拉萨  8.8号
    # start_urls = ['https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2019-08-08&leftTicketDTO.from_station=HFH&leftTicketDTO.to_station=LSO&purpose_codes=ADULT']

    def parse(self, response):
        # 使用下载配置的stations.py，下载到CSV后会乱码 TODO
        # station_dict = stations.dicts
        station_dict = station_info.get_station()  # 被迫使用这个，会请求站点的js
        reserve_station = dict(zip(station_dict.values(), station_dict.keys()))

        # 解析服务器响应的JSON字符串
        json_result = json.loads(response.text)
        # 判断有无出发地--目的地的车次信息
        if json_result['data']['map']:
            # 有该车次信息，提取result里的班次信息
            query_infos = json_result['data']['result']
            # 遍历
            for info in query_infos:
                item = TrainqueryspiderItem()
                # 用|分割结果
                train_infos = info.split('|')
                # 火车出发地和乘客出发地比较
                start_flag = self._get_station_status(train_infos[4], train_infos[6], True)
                # 火车目的地和乘客目的地比较
                end_flag = self._get_station_status(train_infos[5], train_infos[7], False)
                # 车次
                item['train_number'] = train_infos[3]
                #   出发站名称
                item['departure_station'] = reserve_station[train_infos[6]] + '({})'.format(start_flag)
                #   到达站名称
                item['arrival_station'] = reserve_station[train_infos[7]] + '({})'.format(end_flag)
                #   出发时间
                item['departure_time'] = train_infos[8]
                #   到达时间
                item['arrival_time'] = train_infos[9]
                #   历时
                item['need_time'] = train_infos[10]
                #   商务座/特等座
                item['business_class'] = train_infos[32] or train_infos[25] or '--'
                #  一等座
                item['first_class'] = train_infos[31] or '--'
                #   二等座
                item['second_class'] = train_infos[30] or '--'
                #   高级软卧
                item['private_soft'] = train_infos[21] or '--'
                #   软卧/一等卧
                item['first_soft'] = train_infos[23] or '--'
                #   动卧
                item['pssive_seat'] = train_infos[33] or '--'
                #   硬卧/二等卧
                item['second_soft'] = train_infos[28] or '--'
                #   软座
                item['soft_seat'] = train_infos[24] or '--'
                #   硬座
                item['hard_seat'] = train_infos[29] or '--'
                #   备注（是否可预订）
                item['reservation'] = train_infos[1] or '--'
                # 无座
                item['without_seat'] = train_infos[26] or '--'
                #   其他
                item['other'] = train_infos[22] or '--'

                yield item
        else:
            print (u'很抱歉，按您的查询条件，当前未找到从出发地到目的地的列车。')

    '''获取出发站点和达到站点是经过还是始发/终点'''

    def _get_station_status(self, start, end, flag):
        if start == end:
            if flag:
                return '始'
            else:
                return '终'
        else:
            return '过'
