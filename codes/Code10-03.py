## 트리뷰 활용
from tkinter import *
from tkinter import ttk
import csv
from tkinter.filedialog import  *
def openCSV() :
    global  csvList
    filename = askopenfilename(parent=None,
                               filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    csvList = []
    with open(filename)as rfp:
        reader = csv.reader(rfp)
        headerList = next(reader)
        sum = 0
        count = 0
        for cList in reader:
            csvList.append(cList)

    # 기존 시트 클리어
    sheet.delete(*sheet.get_children())

    # 첫번째 열 헤더 만들기
    sheet.column('#0', width=70)  # 첫 컬럼의 내부이름
    sheet.heading('#0', text=headerList[0])
    # 두번째 이후 열 헤더 만들기
    sheet['columns'] = headerList[1:]  # 두분째 이후 컬럼의 내부이름(내맘대로)
    for colName in headerList[1:] :
        sheet.column(colName, width=70)
        sheet.heading(colName, text=colName)

    # 내용 채우기.
    for row in csvList :
      sheet.insert('', 'end', text=row[0], values=row[1:])

    sheet.pack(expand=1, anchor=CENTER)

import xlrd
def openExcel() :
    global  csvList
    filename = askopenfilename(parent=None,
                               filetypes=(("엑셀 파일", "*.xls;*.xlsx"), ("모든 파일", "*.*")))
    csvList = []
    workbook = xlrd.open_workbook(filename)

    print(workbook.nsheets)
    wsList = workbook.sheets()
    headerList = []
    for i in range(wsList[0].ncols) :
        headerList.append(wsList[0].cell_value(0,i))
    print(headerList)

    # 내용 채우기
    for wsheet in wsList :
        rowCount = wsheet.nrows
        colCount = wsheet.ncols
        for i in range(1, rowCount) :
            tmpList = []
            for k in range(0, colCount) :
                tmpList.append(wsheet.cell_value(i,k))
            csvList.append(tmpList)

    # 기존 시트 클리어
    sheet.delete(*sheet.get_children())

    # 첫번째 열 헤더 만들기
    sheet.column('#0', width=70)  # 첫 컬럼의 내부이름
    sheet.heading('#0', text=headerList[0])
    # 두번째 이후 열 헤더 만들기
    sheet['columns'] = headerList[1:]  # 두분째 이후 컬럼의 내부이름(내맘대로)
    for colName in headerList[1:] :
        sheet.column(colName, width=70)
        sheet.heading(colName, text=colName)

    # 내용 채우기.
    for row in csvList :
      sheet.insert('', 'end', text=row[0], values=row[1:])

    sheet.pack(expand=1, anchor=CENTER)

window = Tk()
window.geometry('600x500')

sheet = ttk.Treeview(window)

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="CSV 처리", menu=fileMenu)
fileMenu.add_command(label="CSV 열기", command=openCSV)
fileMenu.add_command(label="엑셀 열기", command=openExcel)
fileMenu.add_separator()



window.mainloop()