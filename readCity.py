import xlrd
import xlwt

# workbook = xlrd.open_workbook('./cityes.xlsx')
# booksheet = workbook.sheet_by_name('sheet1')
# #print booksheet.row_len(1,1)
# #print booksheet.cell_value(0,1)
# tempFileName = './temp/temp.txt'
# file1 = open(tempFileName,'w')
# for rownum in range(booksheet.nrows):
#     value = booksheet.cell_value(rownum,1)
#     #print(value)
#     #value = value.encode('utf-8').decode('unicode_escape')
#     #value = unicode(value, encoding='utf-8')
#     # cityGroups = value.split('/')
#     # print(cityGroups)
#     file1.write(value + "\n")
# file1.close()
dict = {}
tempFileName = './temp/temp.txt'
with open(tempFileName,'r') as file:
    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip('\n')
        line = line.strip(' ')
        values = line.split(',')
        for value in values:
            if value not in dict:
                dict[value] = 1
            else:
                dict[value] = dict[value] + 1
file.close()

wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet('sheet1')
rowIndex = 0
for (k,v) in dict.items():
    ws.write(rowIndex,0,k)
    ws.write(rowIndex,1,v)
    rowIndex += 1

wb.save('temp/2013.xls')