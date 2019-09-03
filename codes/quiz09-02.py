# Code09-04로 선택된 CSV를 TreeView로 출력하기
from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import * # 입력받기. askinteger
from tkinter.filedialog import * # file dialog
import csv

def readCsv(fname:str) -> list:
    """
    파일이름을 읽어서, 각 줄을 list로 반환합니다.
    :param fname: 읽어들일 csv파일 이름
    :return: csv의 내용이 든 list
    """
    ## 우리회사 평균 연봉은?
    with open(fname) as rfp:
        reader = csv.reader(rfp)
        # headerList = next(reader)
        l = [i for i in reader]
    return l


def showTable(window) -> None:
    """
    csv파일을 읽어서 테이블을 window에 출력합니다.
    :param window: 출력할 대상 main window
    :return:없음
    """
    filename = askopenfilename(
        parent=None, filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    csvList = readCsv(filename)
    ## 트리뷰 활용

    # 첫번째 열 만들기
    sheet.column('#0', width=70)
    sheet.heading('#0', text=csvList[0][0]) # 첫 컬럼의 내부이름
    # 두번째 이후 열 만들기
    sheet['columns'] = [i for i in csvList[0][1:]] # 두 번째 이후 컬럼의 내부 이름(내맘대로)
    for i in csvList[0][1:]:
        sheet.column(i, width=70)
        sheet.heading(i, text=i)
    # 내용 채우기
    for i in csvList[1:]:
        sheet.insert('', 'end', text=i[0], values =i[1:])


if __name__ == "__main__":
    window = Tk()
    window.geometry('800x500')
    sheet = ttk.Treeview(window)

    showTable(window)

    sheet.pack()
    window.mainloop()
