# -*- coding: utf-8 -*-
import sys


def code_utf8():
    print (u'----OK--------将Python的默认编码方式修改为utf-8-------------')
    reload(sys)
    sys.setdefaultencoding('utf-8')
