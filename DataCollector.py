#!/usr/bin/python
# -*- coding:utf8 -*-
import  urllib2
import xml.sax
import urllib
import json
import xlwt
import os

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
            uArray = u.split(',')
            if len(uArray) < 3:
                cityStr += u + '/'
            else:
                cityStr += uArray[2] + '/'
        return cityStr
    else:
        unitArray = unit.split(',')
        if len(unitArray) <3:
            return unit + '/'
        else:
            return unitArray[2] + '/'


def getIssueDictFromJson(jsonData):
    issueDict = {}
    yearNum = '0'
    for line in jsonData:
        if line['field'] != '':
            if line['field'] == 'common_year':
                yearNum = line['name']
                issueDict[yearNum] = []
            elif line['field'] == 'issue_num':
                issueDict[yearNum].append(line['name'])
    return issueDict

def yearTreeRequest(journalName):
    url = 'http://www.wanfangdata.com.cn/perio/yearTree.do'
    data = {'perio_id': journalName}
    data_urlencode = urllib.urlencode(data)
    req = urllib2.Request(url=url, data=data_urlencode)
    resData = urllib2.urlopen(req)
    return resData.read()

def atrticlesDataRequest(year, issueNum, perioId, retry=0):
    url = 'http://www.wanfangdata.com.cn/perio/articleList.do'
    data = {'page':'1', 'pageSize':'1000', 'issue_num': issueNum, 'publish_year': year, 'perio_id': perioId}
    data_urlencode = urllib.urlencode(data)
    req = urllib2.Request(url=url, data=data_urlencode)
    try:
        resData = urllib2.urlopen(req, timeout=5)
        res = resData.read()
    except Exception, e:
        retry += 1
        if retry >=4:
            return None
        print 'timeout retry '+ str(retry)
        return atrticlesDataRequest(year,issueNum,perioId, retry)
    return res


#journalList = ['kxtb','qhdxxb','zgkx-ce','bjdxxb','zngydxxb','zjdxxb-gx','tjdxxb','hebgydxxb','dndxxb','hzlgdxxb','shjtdxxb','xtgcllysj','zgkjsl','sxxb','zgkx-ca','lxxb','bzycj','wlxb','gxxb','fxhx','gdxxhxxb','twxb','chxb','dqwlxb','daqikx','ysxb98','dizhixb','kcdz','hyxb','dlxb','dlyj','stxb','swdyx','zwstxb','slxb-','zhyx','dsjydxxb','dyjydxxb','zgyxkxyxb','zhlxbx','zgwsjj','yjfx','gt','jsxb','jsxb','xyjsclygc','jxgcxb','mcxxb','zgjxgc','hzyxb','nrjxb']
#journalList = ['yznkxjs','zgdjgcxb','dlxtzdh','dwjs','dianzixb','dzkxxk','hwyjggc','dbkxxb','jsjxb','rjxb','zdhxb','gfzclkxygc','hxxb','gsyxb','slgy','rlhxxb','dlqgyxyxb','mfzjs','spkx','spyfx','yckj','zgpg','mcgy','zgzz','zgysybzyj']
journalList = ['bjfzxyxb','yslxygcxb','jzjgxb','ytgcxb','ytlx','slxb','skxjz','jtysgcxb','zgtdkx','zgglxb','zgzc','hkxb','tjjs','hjkx','hjkxxb','zgaqkxxb']
yearList = ['2006']
failedList = []
for journalName in journalList:
    print journalName
    yearTreeData = json.loads(yearTreeRequest(journalName))
    issueDict = getIssueDictFromJson(yearTreeData)
    for year in yearList:
        print "|" + year
        if year in issueDict:
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('sheet1')
            rowIndex = 0
            for issueNum in issueDict[year]:
                print "||" + issueNum
                articleJson = atrticlesDataRequest(year,issueNum,journalName)
                if articleJson == None:
                    failedList.append(journalName + '/' + year + '/' + issueNum)
                else:
                    articlesData = json.loads(articleJson)
                    for row in articlesData['pageRow']:
                        if 'authors_unit' in row:
                            ws.write(rowIndex,0,issueNum)

                            if 'title' in row:
                                ws.write(rowIndex, 1, row['title'])
                            else:
                                ws.write(rowIndex,1,'N/A')
                            if 'authors_name' in row:
                                ws.write(rowIndex, 2, row['authors_name'])
                            else:
                                ws.write(rowIndex,2,'N/A')
                            ws.write(rowIndex,3,row['authors_unit'])
                            ws.write(rowIndex,4,unitsToCities(row['authors_unit']))
                            if 'fund_info' in row:
                                ws.write(rowIndex,5,row['fund_info'])
                            else:
                                ws.write(rowIndex,5,'N/A')
                            rowIndex += 1

            if not os.path.exists('newData/' + year):
                os.mkdir('newData/' + year)
            wb.save('newData/' +  year + '/' + journalName + '.xls')

if len(failedList) >0:
    print 'Failed list:'
    for value in failedList:
        print value