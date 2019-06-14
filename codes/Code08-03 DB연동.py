from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import pymysql
####################
#### 전역 변수부 ####
####################
IP_ADDR = '192.168.56.107'; USER_NAME = 'root'; USER_PASS = '1234'
DB_NAME = 'BigData_DB'; CHAR_SET = 'utf8'
####################
#### 함수부 ####
####################
def selectFile() :
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    edt1.insert(0, str(filename))

import datetime
def uploadData() :
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    fullname = edt1.get()
    with open(fullname, 'rb') as rfp :
        binData = rfp.read()
    fname = os.path.basename(fullname)
    fsize = os.path.getsize(fullname)
    height = width = int(math.sqrt(fsize))
    now = datetime.datetime.now()
    upDate = now.strftime('%Y-%m-%d')
    upUser = USER_NAME
    sql = "INSERT INTO rawImage_TBL(raw_id , raw_height , raw_width"
    sql += ", raw_fname , raw_update , raw_uploader, raw_avg , raw_data) "
    sql += " VALUES(NULL," + str(height) + "," + str(width) + ",'"
    sql += fname + "','" + upDate +"','" + upUser + "',0 , "
    sql += " %s )"
    tupleData = (binData,)
    cur.execute(sql, tupleData)
    con.commit()
    cur.close()
    con.close()
    print(sql)

import tempfile
def downloadData() :
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    sql = "SELECT raw_fname, raw_data FROM rawImage_TBL WHERE raw_id = 1"
    cur.execute(sql)
    fname, binData = cur.fetchone()

    fullPath = tempfile.gettempdir() + '/' + fname
    with open(fullPath, 'wb') as wfp :
        wfp.write(binData)
    print(fullPath)
    cur.close()
    con.close()
    print(sql)
####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x200")
window.title("Raw --> DB Ver 0.02")

edt1 = Entry(window, width=50); edt1.pack()
btnFile = Button(window, text="파일선택", command=selectFile); btnFile.pack()
btnUpload = Button(window, text="업로드", command=uploadData); btnUpload.pack()

btnDownload = Button(window, text="다운로드", command=downloadData); btnDownload.pack()


window.mainloop()