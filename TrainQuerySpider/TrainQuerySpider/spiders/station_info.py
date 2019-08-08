# -*- coding: utf-8 -*-
import requests
import re
import json
import os

'''获取12306各个站点的信息，转换成字典格式'''


def get_station():
    station_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9108'
    # 关闭站点证书的提示
    requests.packages.urllib3.disable_warnings()
    # 发送请求并校验返回结果的格式
    response = requests.get(station_url, verify=False)
    '''方法一'''
    # 正则校验
    # result = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
    # 转换成字典格式,key：车站名name，value：code
    # station = dict(result)
    '''方法二'''
    # 定义字典
    station = {}
    # 去掉开头并以@符号分割
    r = response.text.strip("var station_names =';")
    result_list = r.split('@')[1:]
    # 遍历并组成字典元素
    for item in result_list:
        temp = item.split('|')
        station[temp[1]] = temp[2]
    return station


'''将站名的信息保存到本地'''


def save_station(paths):
    # paths = os.getcwd() + '\\12306'
    if not os.path.exists(paths):
        # 不存在就创建该路径
        os.mkdir(paths)
        print(u'----OK-------------文件路径：{}---->创建成功-----------------').format(paths)
        # 将字典数据以json字符串格式保存到本地
        stations_dict = get_station()
        stations_json = json.dumps(stations_dict, ensure_ascii=False)
        try:
            with open(paths + '\\stations.txt', 'w') as fw:
                fw.write(stations_json)
                print (u'----OK-------------数据成功写入stations.txt中-----------------')
        except Exception as e:
            print e
        # return stations_dict
    # else:
    #     try:
    #         with open(paths + '\\stations.txt', 'r') as fr:
    #             stations_json = fr.read()
    #             print (u'数据查询成功....')
    #     except Exception as e:
    #         print e
    #     # 将json字符串转化为字典
    #     stations_dict = json.loads(stations_json)
    #     return stations_dict
