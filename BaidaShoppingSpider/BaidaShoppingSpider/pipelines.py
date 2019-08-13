# -*- coding: utf-8 -*-
import csv
import json
import codecs
import os
import datetime
import sys
from spiders import good_dict_setting
# 需要pip安装openpyxl模块
from openpyxl import Workbook
# mysql驱动
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 解决这个报错：'ascii' codec can't encode characters in position 0-3: ordinal not in range(128)
reload(sys)
sys.setdefaultencoding('gbk')


class BaidashoppingspiderPipeline(object):

    def __init__(self):
        print(u'------------选择导出的格式：a-csv,b-excel,c-txt,d-json,e-xml,f-word,g-pdf，h-mysql,i-mongodb,j-oracle')
        # 输入需要导出的格式
        self.input_style = raw_input()

        # 指定输出路径
        self.now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.out_paths = self.choose_export_path()

        # 文件头部
        self.file_header = [u'商品类型', u'商品名称属性', u'商品价格', u'商品图片', u'配送店家', u'商品详情链接']

        # 选择输出不同文件格式
        if self.input_style == 'a':  # csv
            # 解决输出有空行情况，读写模式Python2.x中必须为wb，Python3.x可以用newline=''
            if sys.version < '3':
                self.writer = csv.writer(open(self.out_paths, 'wb'))
            else:
                # TypeError: 'newline' is an invalid keyword argument for this function
                self.writer = csv.writer(open(self.out_paths, 'w', newline=''))
            # 添加表头
            self.writer.writerow(self.file_header)
        elif self.input_style == 'b':  # excel
            # 实例化工作簿并激活
            self.wb = Workbook()
            self.ws = self.wb.active
            # 添加表头
            self.ws.append(self.file_header)
        elif self.input_style == 'c':  # txt
            pass
        elif self.input_style == 'd':  # json
            self.json_data = codecs.open(self.out_paths, 'w')
        elif self.input_style == 'h':  # mysql
            # 创建数据库连接,记得先开启mysql服务
            self.db = pymysql.connect(
                host='localhost',
                port=3306,
                db='book-numberlist',
                user='xxwei3',
                passwd='123123',
                charset='utf8mb4',  # 设置编码类型
                cursorclass=pymysql.cursors.DictCursor  # 设置游标类型
            )
            # 存在先删除该表
            curs = self.db.cursor()
            sql = 'drop table if exists good_info'
            # 报错：InterfaceError: (0, '')
            curs.execute(sql)
            # 创建表
            table_sql = '''
                        create table good_info(
                            good_type VARCHAR(32) NOT NULL,
                            good_alt VARCHAR(100),
                            good_price VARCHAR(32),
                            good_picture VARCHAR(100),
                            hotel VARCHAR(32),
                            good_detail_url VARCHAR(100)
                        )
                        '''
            curs.execute(table_sql)
            print(u'---------------------->表已经创建,create table ok')
            # curs.close()

    def process_item(self, item, spider):
        result_data = [item['good_type'], item['good_alt'], item['good_price'],
                       item['good_picture'], item['hotel'], item['good_detail_url']]
        # 添加数据
        if self.input_style == 'a':  # csv
            self.writer.writerow(result_data)
        elif self.input_style == 'b':  # excel
            self.ws.append(result_data)
            # 指定数据保存路径
            self.wb.save(self.out_paths)
        elif self.input_style == 'c':  # txt
            # print ('------------------>', result_data)
            # txt文本文件模式设置为w会覆盖，因此使用追加的方式
            with open(self.out_paths, 'a') as fw:
                enter_symbol = '\n'
                colon_symbol = ':'
                spilt_symbol = '**************************************************************' + enter_symbol
                raw1 = self.file_header[0] + colon_symbol + result_data[0] + enter_symbol
                raw2 = self.file_header[1] + colon_symbol + result_data[1] + enter_symbol
                raw3 = self.file_header[2] + colon_symbol + result_data[2] + enter_symbol
                raw4 = self.file_header[3] + colon_symbol + result_data[3] + enter_symbol
                raw5 = self.file_header[4] + colon_symbol + result_data[4] + enter_symbol
                raw6 = self.file_header[5] + colon_symbol + result_data[5] + enter_symbol
                txt_list = [spilt_symbol, raw1, raw2, raw3, raw4, raw5, raw6]
                # 写入整个列表
                fw.writelines(txt_list)
        elif self.input_style == 'd':  # json
            json_data = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.json_data.write(json_data)
        elif self.input_style == 'h':  # mysql
            # 插入数据
            self._insert(result_data)
            print(u'---------------------->表数据已成功插入,insert data ok')

        return item

    def choose_export_path(self):
        '''选择文件的格式'''
        style_list = good_dict_setting.good_type_dicts.get(self.input_style)
        style_file_name = style_list[0]
        style_suffix = style_list[1]
        print (u'文件格式：', style_file_name)
        # 指定文件的路径
        paths = os.getcwd() + u'\BaidaShoppingSpider\\{}'.format(style_file_name)
        # 不存在对应目录则创建
        if not os.path.exists(paths):
            os.mkdir(paths)
        # 文件的输出路径
        out_paths = paths + u'\\bdysc_{}{}'.format(self.now_time, style_suffix)
        print (u'文件的输出路径---->', out_paths)
        return out_paths

    def _insert(self, result_data):
        '''插入数据'''
        # 创建游标
        cur = self.db.cursor()
        try:
            # 执行sql插入语句
            # cur.execute(
            #     'insert into good_info values (%s,%s,%s,%s,%s,%s)' % (
            #         result_data[0], result_data[1], result_data[2],
            #         result_data[3], result_data[4], result_data[5])
            # )
            # 报错：InternalError: (1366, u"Incorrect string value: '\\xD6\\xC7\\xC4\\xDC\\xC9\\xE8...' for column 'good_type' at row 1")
            # sql语句写的存在问题
            cur.execute(
                "insert into good_info(good_type,good_alt,good_price,good_picture,hotel,good_detail_url) \
                values ({},{},{},{},{},{})".format(
                    pymysql.escape_string(result_data[0]),
                    pymysql.escape_string(result_data[1]),
                    pymysql.escape_string(result_data[2]),
                    pymysql.escape_string(result_data[3]),
                    pymysql.escape_string(result_data[4]),
                    pymysql.escape_string(result_data[5]))
            )
            # 提交
            self.db.commit()
        except Exception as e:
            # 失败需要回滚操作
            print e
            self.db.rollback()
        finally:
            # 关闭资源连接
            # self.db.close()
            # cur.close()
            pass
