# -*- coding: utf-8 -*-
import messy_code
import station_info
import stations

'''用户输入查询条件进行自定义查询'''


def query_custom():
    # 将Python的默认编码方式修改为utf-8
    messy_code.code_utf8()

    # 用于交互的控制台输入
    print(u'----OK--------输入您要查询条件获取详细的车票详细------------')
    print(u'请输入出发站点：')
    from_station = raw_input()  # value-->HFH
    from_station = from_station.decode('gbk').encode('utf-8')  # 解决这个编解码问题好头痛~~

    print(u'请输入到达站点：')
    to_station = raw_input()  # value-->FYH
    to_station = to_station.decode('gbk').encode('utf-8')

    print(u'请输入出发日期(格式如2019-08-01)：')
    time = raw_input()

    print(u'请输入查询类型（成人票输入1，学生票输入2）：')
    purpose_code = raw_input()  # 默认成人票ADULT，0X00表示学生票

    # 构造请求接口的URL
    # 排查打印，均为False
    # print from_station == '阜阳'
    # print from_station == u'阜阳'
    # print from_station == '\u961c\u9633'
    # print from_station == u'\u961c\u9633'

    # 备注下：这里被编码弄的头昏脑胀，from_station和to_station无法在字典里get到，目前已解决~
    station_list = __get_code_by_name(from_station, to_station)
    purpose_code = __process_purpose_code(purpose_code)

    print station_list[0]  # None
    print station_list[1]  # None
    print purpose_code

    start_url = 'https://kyfw.12306.cn/otn/leftTicket/query?' \
                'leftTicketDTO.train_date={}&' \
                'leftTicketDTO.from_station={}' \
                '&leftTicketDTO.to_station={}' \
                '&purpose_codes={}'.format(time, station_list[0], station_list[1], purpose_code)
    print (u'----OK--------即将访问的接口地址为--->' + str(start_url))
    return start_url


'''成人票和学生票'''


def __process_purpose_code(str_number):
    # 异常情况
    if str_number == 'null' or len(str_number) == 0:
        return 'ADULT'  # 默认成人票
    elif str_number == '1':
        return 'ADULT'
    elif str_number == '2':
        return '0X00'


'''根据字典的name获取code'''


def __get_code_by_name(*args):
    lists = []
    dicts = stations.dicts
    for i in args:
        # print i
        code = dicts.get(i)
        print code
        lists.append(code)
    return lists

