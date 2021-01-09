#!/usr/bin/python

import  urllib
import xml.sax
import  urllib2
from xml.dom.minidom import parse
import xml.dom.minidom
import re


journalDict = {}
journalDict['KXTB'] = "科学通报"
journalName = 'KXTB'
year = "2015"
outputFile = open(journalDict[journalName] + 'csv','w')
outputFile.write('year,issue,articlTitle,autors,orgns\n')
outputFile.write('2015')
outputFile.write('01')
outputFile.write('test1')
outputFile.write('autor1 author2')
outputFile.write('orgn1\n')
outputFile.write('2015')
outputFile.close()

###require year list
url = "http://navi.cnki.net/knavi/JournalDetail/GetJournalYearList?pcode=CJFD&pykm="+journalName+"&pIdx=0"
req = urllib2.Request(url)
resData = urllib2.urlopen(req)
res = resData.read()

###write the response buffer to temp file
file_object = open('temp.xml', 'w')
file_object.write(res)
file_object.close()

###read temp file
DOMTree = xml.dom.minidom.parse("temp.xml")
collection = DOMTree.documentElement
years = collection.getElementsByTagName("dl")

###year list
for yearItem in years:
    #print "*******",year.getAttribute("id"),"*********"
    em = yearItem.getElementsByTagName("em")
    yearNum = em.item(0).firstChild.data
    print yearNum
    if yearNum == year:
        ###issue list
        dds = yearItem.getElementsByTagName("dd")
        for dd in dds:
            a = dd.getElementsByTagName("a")
            for aItem in a:
                aItmId = aItem.getAttribute("id")
                issue = aItmId[6:]
                print "| ",issue
                hasArticl = True
                articlIndex = 1
                while hasArticl:
                    if(articlIndex < 10):
                        articlDetailUrl = "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=" + journalName + year + issue + "00"+ str(articlIndex) +"&dbname=CJFDLAST" + year
                    elif(articlIndex>=10 and articlIndex<100):
                        articlDetailUrl = "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=" + journalName + year + issue + "0" + str(articlIndex) + "&dbname=CJFDLAST" + year
                    else:
                        articlDetailUrl = "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=" + journalName + year + issue + str(articlIndex)+"&dbname=CJFDLAST" + year
                    print articlDetailUrl

                    articlReq = urllib2.Request(articlDetailUrl)
                    resData = urllib2.urlopen(articlReq)
                    articlRes = resData.read()

                    titleObj = re.search(r'<h2\s*class="title".*?h2>',articlRes)
                    if titleObj == None:
                        break
                    print titleObj.group()
                    authorDiv = re.search(r'<div\s*class="author".*?div>',articlRes)
                    authorList = re.findall(r'>[^<][^>]+?<',authorDiv.group())
                    for author in authorList:
                        print author
                    orgnDiv = re.search(r'<div\s*class="orgn".*?div>', articlRes)
                    orgnList = re.findall(r'>[^<][^>]+?<',orgnDiv.group())
                    for orgn in orgnList:
                        print orgn
                    # fundDiv = re.search(r'<p>.*catalog_FUND. *?</p>', articlRes)
                    # if fundDiv:
                    #     print fundDiv.group()
                    ###write the response buffer to temp file
                    # file_object = open('fileDetail'+str(articlIndex)+'.xml', 'w')
                    # file_object.write(articlRes)
                    # file_object.close()
                    #
                    # ###read temp file
                    # DOMTree = xml.dom.minidom.parse("fileDetail.xml")
                    # collection = DOMTree.documentElement
                    #years = collection.getElementsByTagName("dl")
                    articlIndex+=1