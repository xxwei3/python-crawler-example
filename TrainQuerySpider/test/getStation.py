# 测试地市js数据是否可以正常访问
import requests
import re

def getStation():
	url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9108'
	r = requests.get(url, verify=False)
	result = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', r.text)
	station = dict(result)
	print(station)
	return station

def main():
	# 关闭站点证书的提示
	requests.packages.urllib3.disable_warnings()
	getStation()

if __name__ == '__main__':
    main()
