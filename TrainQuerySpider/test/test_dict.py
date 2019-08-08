# -*- coding: utf-8 -*-

print(u'请输入出发站点：')
from_station = raw_input()  # HFH

print(u'请输入到达站点：')
to_station = raw_input()  # FYH

station_kv = {'合肥': 'HFH', '阜阳': 'FYH', '芜湖': 'WHH','hefei': 'HFH','fuyang': 'FYH'}

print station_kv.get(from_station.decode('gbk').encode('utf-8'))
print station_kv.get(to_station.decode('gbk').encode('utf-8'))