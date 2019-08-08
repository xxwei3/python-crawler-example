# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TrainqueryspiderPipeline(object):
    def process_item(self, item, spider):
        print('1',item['train_number'])
        print('1', item['departure_station'])
        print('1', item['arrival_station'])
        print('1', item['departure_time'])
        print('1', item['arrival_time'])
        print('1', item['need_time'])
        print('1', item['first_class'])
        print('1', item['second_class'])
        print('1', item['first_soft'])
        print('1', item['second_soft'])
        print('1', item['hard_seat'])
        print('1', item['without_seat'])
        print('1', item['business_class'])
        print('1', item['pssive_seat'])
        print ('1',item['other'])
        print ('1', item['reservation'])
        print ('1', item['private_soft'])
        print('1', item['soft_seat'])
        return item
