#!/usr/bin/python
#coding=utf-8
import  urllib2
from xml.dom.minidom import parse
import xml.dom.minidom
import re
import time
import  xlwt
import  os


def cutHeadTail(oldStr):
    return oldStr[1:len(oldStr)-1]

def titleFormer(oldTitle):
    searchObj = re.search(r'>.*?</',oldTitle)
    return cutHeadTail(searchObj.group())


#journalList = ['JEXK','KXTB','QHXB','XAJT','BJDZ','ZNGD','ZDZC','TJDZ','HEBX','DNDX','HZLG','SHJT','XTLL','ZGKS','YSXB','DZXE','KCDZ','SEAC','DLXB','DWJS','SXXB','JAXK','LXXB','BZCJ','WLXB','GXXB','FXHX','GDXH','TWXB','CHXB','DQWX','DQXK','DLYJ','STXB','SWDY','ZWSB','SLXX','ZHYX','DSDX','DYJD','ZYKX','ZHLX','WEIJ','ZHYF','ZCYO','ZGZY','ZRSZ','ZJSB','ZYXX','ZGKF','ZHXX','ZHJH','ZHWK','ZHGK','ZGWK','ZHFC','ZHEK','ZHZL','ZHSJ','ZHPF','ZHEB','ZHYK','ZHKY','ZHGS','YXXB','ZGYX','ZNYK','HBNB','GHDQ','TRXB','NYGU','XBZW','ZGSK','ZWBL','YYXB']
journalList = ['LYKE','LYKX','XMSY','ZGXQ','CYXB','SCKX','DWYC','FUHE','BZGC','SXJS','ZLXB','ZKKX','JLXB','ZGKD','MTXB','SYXB','SKYK','TRQG','YJFX','GANT','JSXB','ZYXZ','COSE','JXXB','MCXX','ZGJX','BGXB','NRJX','YZJS','ZGDC','DLXT','DZXU','DZYX','HWYJ','DBKX','JSJX','RJXB','MOTO','GFZC','HXXB','GXYB','SLGY','RLHX','DLQG','MFJS','SPKX','SPFX','YCKJ','ZGPG','MCGY','ZGZZ','SZYS','BFXB','YSLX','JZJB','YTGC','YTLX','SLXB','SKXJ','JYGC','ZGTK','ZGGL','ZGZC','HKXB','TJJS','HJKZ','HJXX','ZAQK']
year = '2015'

startTime = time.asctime( time.localtime(time.time()) )

# wb = xlwt.Workbook(encoding='utf-8')
# ws = wb.add_sheet('sheet1')
# rowIndex =0
for journalName in journalList:

    print journalName
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(journalName)
    # ws.write(0,0,'年份')
    # ws.write(0,1,'期号')
    # ws.write(0,2,'标题')
    # ws.write(0,3,'作者')
    # ws.write(0,4,'单位')
    # ws.write(0,5,'城市')
    # ws.write(0,6,'基金')
    # ws.write(0,7,'链接')

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

    rowIndex = 0
    for yearItem in years:
        em = yearItem.getElementsByTagName('em')
        yearNum = em.item(0).firstChild.data
        if yearNum == year:
            #print yearNum
            issueList = yearItem.getElementsByTagName('a')
            for issueItem in issueList:
                issueId = issueItem.getAttribute('id')
                issueNum = issueId[6:]
                print "||" , issueNum
                articlIndex = 1
                while 1:
                    if articlIndex< 10:
                        articlDetailUrl = "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=" + journalName + year + issueNum + "00"+ str(articlIndex) +"&dbname=CJFDLAST" + year
                    elif articlIndex>=10 and articlIndex<100:
                        articlDetailUrl = "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=" + journalName + year + issueNum + "0" + str(articlIndex) + "&dbname=CJFDLAST" + year
                    else:
                        articlDetailUrl = "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=" + journalName + year + issueNum + str(articlIndex)+"&dbname=CJFDLAST" + year
                    #print articlDetailUrl

                    articlReq = urllib2.Request(articlDetailUrl)
                    resData = urllib2.urlopen(articlReq)
                    articlRes = resData.read()


                    titleObj = re.search(r'<h2\s*class="title".*?h2>', articlRes)
                    if titleObj == None:
                        break
                    #outputFile.write(yearNum + ',' + issueNum + ',')
                    rowIndex += 1
                    ws.write(rowIndex,0,journalName)
                    ws.write(rowIndex,1,yearNum)
                    ws.write(rowIndex,2,issueNum)

                    #print titleObj.group()
                    title = titleFormer(titleObj.group())
                    ws.write(rowIndex,3,title)
                    #outputFile.write(title+',')
                    authorDiv = re.search(r'<div\s*class="author".*?div>', articlRes)
                    authorList = re.findall(r'>[^<][^>]+?<', authorDiv.group())
                    authors = ''
                    for author in authorList:
                        authors += cutHeadTail(author) + '/'
                    ws.write(rowIndex,4,authors)

                        #print author
                        #outputFile.write(cutHeadTail(author) + '/')
                    #outputFile.write(',')
                    orgnDiv = re.search(r'<div\s*class="orgn".*?div>', articlRes)
                    orgnList = re.findall(r'>[^<][^>]+?<', orgnDiv.group())
                    orgns = ''
                    orgnNum = 0
                    for orgn in orgnList:
                        orgn = orgn.strip('<')
                        orgn = orgn.strip('>')
                        orgns += orgn + '/'
                        orgnNum += 1
                        if orgnNum >= 3:
                            break
                        #print orgn
                        #outputFile.write(cutHeadTail(orgn) + '/')
                    #outputFile.write(',,' + articlDetailUrl + '\n')
                    ws.write(rowIndex,5,orgns)

                    fundDiv = re.search(r'<label id="catalog_FUND">基金：</label>[\s\S]*?</p',articlRes)
                    if fundDiv != None:
                        fundList = re.findall(r"'.*?\(.*?\)", fundDiv.group())
                        funds = ''
                        for fund in fundList:
                            fund.strip('\'')
                            fund.strip('fu')
                            fund.strip(' ')
                            funds += fund + '/'
                        ws.write(rowIndex,6,funds)
                    #ws.write(rowIndex,7,articlDetailUrl)
                    articlIndex += 1
            break
    #outputFile.close()
    folder = os.path.exists('data/'+ year)
    if not folder:
        os.mkdir('data/'+year)
    wb.save('data/'+year+'/' +journalName+ '.xls')
endTime = time.asctime( time.localtime(time.time()) )
print "StartTime: ", startTime
print "EndTime: ",endTime