#!/usr/bin/python
# -*- coding:utf8 -*-
import  urllib2
import xml.sax
import urllib
import json
from xml.dom.minidom import parse
import xml.dom.minidom
import  re
import importlib
import sys


def unitsToCities(authorsUnit):
    if isinstance(authorsUnit,list):
        cityStr = ''
        for unit in authorsUnit:
            cityStr += unitsToCity(unit)
        return cityStr
    else:
        return unitsToCity(authorsUnit)

def unitsToCity(unit):
    unitStr = unit.split(';')
    if isinstance(unitStr, list):
        cityStr = ''
        for u in unitStr:
            cityStr += u.split(',')[2] + '/'
        return cityStr
    else:
        return unit.split(',')[2] + '/'



journalList = ['xajtdxxb']
url = 'http://www.wanfangdata.com.cn/perio/articleList.do'
data = {'page':'1','pageSize':'100','issue_num':'1','publish_year':'2018','perio_id':'xajtdxxb'}
data_urlencode = urllib.urlencode(data)
req = urllib2.Request(url=url, data=data_urlencode)
resData = urllib2.urlopen(req)
res = resData.read()

jsonData = json.loads(res)
for row in jsonData['pageRow']:
    if 'authors_unit' in row:
        print unitsToCities(row['authors_unit'])
#读取年份刊次列表
# issueDict = {}
# jsonData = json.loads(res)
# yearNum = 0
# for line in jsonData:
#     if line['field'] != '':
#         if line['field'] == 'common_year':
#             yearNum = line['name']
#             issueDict[yearNum] = []
#         elif line['field'] == 'issue_num':
#             issueDict[yearNum].append(line['name'])
