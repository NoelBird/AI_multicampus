import csv


## 우리회사 평균 연봉은?
with open('c:/images/csv/emp.csv') as rfp:
    reader = csv.reader(rfp)
    headerList = next(reader)

    sum = 0
    count = 0
    for cList in reader:
        sum += int(cList[3])
        count += 1
    avg = sum // count
    print(avg)
# l = []
# with open('c:/images/csv/emp.csv') as rfp:
#     while True:
#         line = rfp.readline()
#         if not line:
#             break
#         l.append(line)
#
# wageList = [int(i.strip().split(',')[3]) for i in l[1:]]
# print(sum(wageList)/len(wageList))