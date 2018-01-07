#!/usr/bin/python
#coding=utf-8
import  urllib2
from xml.dom.minidom import parse
import xml.dom.minidom
import re
import codecs


def cutHeadTail(oldStr):
    return oldStr[1:len(oldStr)-1]

def titleFormer(oldTitle):
    searchObj = re.search(r'>.*?</',oldTitle)
    return cutHeadTail(searchObj.group())

journalList = ['QHXB']
year = '2015';


for journalName in journalList:

    outputFile = open('data/'+journalName + '.csv', 'w')
    outputFile.write(codecs.BOM_UTF8)
    outputFile.write('年份,期号,标题,作者,单位,链接\n')

    ###require year list
    url = "http://navi.cnki.net/knavi/JournalDetail/GetJournalYearList?pcode=CJFD&pykm=" + journalName + "&pIdx=0"
    req = urllib2.Request(url)
    resData = urllib2.urlopen(req)
    res = resData.read()

    ###write the response buffer to temp file
    file_object = open('temp/'+journalName + '.xml', 'w')
    file_object.write(res)
    file_object.close()

    ###read temp file
    DOMTree = xml.dom.minidom.parse('temp/'+journalName + '.xml')
    collection = DOMTree.documentElement
    years = collection.getElementsByTagName("dl")

    for yearItem in years:
        em = yearItem.getElementsByTagName('em')
        yearNum = em.item(0).firstChild.data
        if yearNum == year:
            print yearNum
            issueList = yearItem.getElementsByTagName('a')
            for issueItem in issueList:
                issueId = issueItem.getAttribute('id')
                issueNum = issueId[6:]
                print issueNum
                articlIndex = 1
                while 1:
                    if articlIndex< 10:
                        articlDetailUrl = "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=" + journalName + year + issueNum + "00"+ str(articlIndex) +"&dbname=CJFDLAST" + year
                    elif articlIndex>=10 and articlIndex<100:
                        articlDetailUrl = "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=" + journalName + year + issueNum + "0" + str(articlIndex) + "&dbname=CJFDLAST" + year
                    else:
                        articlDetailUrl = "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=" + journalName + year + issueNum + str(articlIndex)+"&dbname=CJFDLAST" + year
                    print articlDetailUrl

                    articlReq = urllib2.Request(articlDetailUrl)
                    resData = urllib2.urlopen(articlReq)
                    articlRes = resData.read()

                    titleObj = re.search(r'<h2\s*class="title".*?h2>', articlRes)
                    if titleObj == None:
                        break
                    outputFile.write(yearNum + ',' + issueNum + ',')

                    print titleObj.group()
                    title = titleFormer(titleObj.group())
                    outputFile.write(title+',')
                    authorDiv = re.search(r'<div\s*class="author".*?div>', articlRes)
                    authorList = re.findall(r'>[^<][^>]+?<', authorDiv.group())
                    for author in authorList:
                        print author
                        outputFile.write(cutHeadTail(author) + '/')
                    outputFile.write(',')
                    orgnDiv = re.search(r'<div\s*class="orgn".*?div>', articlRes)
                    orgnList = re.findall(r'>[^<][^>]+?<', orgnDiv.group())
                    for orgn in orgnList:
                        print orgn
                        outputFile.write(cutHeadTail(orgn) + '/')
                    outputFile.write(',' + articlDetailUrl + '\n')
                    articlIndex += 1
            break
    outputFile.close()