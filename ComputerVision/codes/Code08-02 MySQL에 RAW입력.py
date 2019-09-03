from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import datetime
import pymysql
import tempfile
## tempfile.gettempdir() + '/' +

# 전역 변수부
IP_ADDR = '192.168.56.106'
USER_NAME = 'root'
USER_PASS = '1234'

DB_NAME = 'BigData_DB'
CHAR_SET = 'utf-8'


# 함수부
def selectFile():
    filename = askopenfilename()
    if filename == '' or filename == None:
        return
    edt1.insert(0, str(filename))


def uploadData():
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    fullname = edt1.get()
    with open(edt1.get(), 'rb') as rfp:
        binData = rfp.read()
        fname = os.path.basename(fullname)
        fsize = os.path.getsize(fullname)
        height = width = int(math.sqrt(fsize))
        now = datetime.datetime.now()
        upData = now.strftime('%Y-%m-%d')
        upUser = USER_NAME
        sql = "INSERT INTO rawImage_TBL(raw_id, raw_height, raw_width"
        sql += ", raw_fname, raw_update, raw_uploader, raw, avg, raw_data)"
        sql += "VALUES(NULL, " + height + "," + width + "'" + fname + "'"
        sql += upData + "','" + upUser + "',0, %s)"
        tupleData = (binData,) # 대용량 데이터는 튜플로 만들어서 매치를 시켜서 넣어야함.
        cur.execute(sql, tupleData)

        con.commit()
        cur.close()
        con.close()


# 메인코드부

window = Tk()
window.geometry("500x500")
window.title("Raw --> DB Ver 0.02")

edt1 = Entry(window, width=50)
edt1.pack()

btnFile = Button(window, text="파일선택", command=selectFile)
btnFile.pack()

btnUpload = Button(window, text="업로드", command=uploadData)
btnUpload.pack()

window.mainloop()