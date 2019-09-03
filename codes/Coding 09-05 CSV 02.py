import csv
from tkinter.filedialog import *

## 우리회사 평균 연봉은?

filename = askopenfilename(
    parent=None, filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
csvList = []
with open(filename) as rfp:
    reader = csv.reader(rfp)
    headerList = next(reader)

    sum = 0
    count = 0
    for cList in reader:
        csvList.append(cList)
## 가격을 10% 인상시키기.
#1. Cost 열의 위치를 찾아내기
headerList = [data.upper().strip() for data in headerList]
pos = headerList.index('COST')
for i in range(len(csvList)):
    rowList = csvList[i]
    cost = rowList[pos]
    cost = float(cost[1:])
    cost *= 1.1
    costStr = "${0:.2f}".format(cost)
    csvList[i][pos] = costStr
print(csvList)

## 결과를 저장하기

saveFp = asksaveasfile(parent=None, mode='wt',
                       filetypes=(("CSV파일", "*.csv"), ("모든파일", "*.*")), defaultextension='.csv')
with open(saveFp.name, mode='w', newline='') as wFp:
    writer = csv.writer(wFp)
    writer.writerow(headerList)
    for row in csvList:
        writer.writerow(row)
