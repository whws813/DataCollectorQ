import os
import xlrd
import xlwt

journalNumMax = 15
folderName = '2013'

wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet('sheet1')
rowIndex = 0
journalNum = 0;
for file in os.listdir('newData/'+folderName):
    if '.xls' in os.path.basename(file):
        journalNum += 1
        if journalNum > journalNumMax:
            break
        workbook = xlrd.open_workbook('newData/'+folderName +'/' + file)
        sheet = workbook.sheet_by_index(0)
        if sheet.nrows == 0:
            print folderName + '/' + file + " is empty!!!!"
        else:
            ws.write(rowIndex,0,file)
            rowIndex+=1
            for rowNum in range(0, sheet.nrows):
                ws.write(rowIndex, 0, sheet.cell_value(rowNum, 3))
                ws.write(rowIndex, 1, sheet.cell_value(rowNum, 4))
                rowIndex += 1
wb.save('total/' + folderName + '.xls')
