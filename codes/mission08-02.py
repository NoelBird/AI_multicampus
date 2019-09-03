from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path

#####################
#### 전역 변수부 ####
#####################
IP_ADDR = '192.168.56.107'
USER_NAME = 'root'
USER_PASS = '1234'
DB_NAME = 'BigData_DB'
CHAR_SET = 'utf8'


################
#### 함수부 ####
################
def getPathList(folderFullName: str) -> list:
    """
    특정 폴더의 전체 파일을 리스트 형태로 반환합니다.
    :param folderFullName:파일명을 가져올 대상 경로. 절대경로
    :return: 대상 경로 안에 들어있는 모든 경로들을 절대 경로로 반환(list)
    """
    fullNameList = []
    for dirName, subDirList, fnames in os.walk(folderFullName):
        for fname in fnames:
            fullName = os.path.join(dirName, fname)
            fullNameList.append(fullName)
    return fullNameList


import pymysql
import datetime
def uploadRawImage() -> None:
    """
    특정 폴더를 지정해서 일괄적으로 RAW파일을 원격 DB에 저장합니다.
    :return:없음
    """
    filename = askdirectory(parent=window)

    fullNameList = getPathList(filename)

    rawFileList = [i for i in fullNameList if os.path.splitext(i)[1].lower() == '.raw']

    for rawFile in rawFileList:
        con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                              db=DB_NAME, charset=CHAR_SET)
        cur = con.cursor()
        fullname = rawFile
        with open(fullname, 'rb') as rfp:
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
        sql += fname + "','" + upDate + "','" + upUser + "',0 , "
        sql += " %s )"
        tupleData = (binData,)
        cur.execute(sql, tupleData)
        con.commit()
        cur.close()
        con.close()


def malloc(h, w, initValue=0) :
    retMemory= []
    for _ in range(h) :
        tmpList = []
        for _ in range(w) :
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory


def getImageDetails(fname) -> tuple:

    fsize = os.path.getsize(fname)  # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize))  # 핵심 코드
    ## 입력영상 메모리 확보 ##
    inImage = []
    inImage = malloc(inH, inW)
    # 파일 --> 메모리
    with open(fname, 'rb') as rFp:
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rFp.read(1)))

    flatData = [inImage[i][k] for i in range(inH) for k in range(inW)]
    avgImage = sum(flatData)//(inH*inW)
    maxImage = max(flatData)
    minImage = min(flatData)

    return avgImage, maxImage, minImage


def uploadDetailRawImage():
    """

    :param fullNameList:raw파일이 들어있는 경로의 모든 파일
    :return:없음
    """

    filename = folder = askdirectory(parent=window)

    fullNameList = getPathList(filename)

    rawFileList = [i for i in fullNameList if os.path.splitext(i)[1].lower() == '.raw']

    for rawFile in rawFileList:
        con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                              db=DB_NAME, charset=CHAR_SET)
        cur = con.cursor()
        fullname = rawFile
        with open(fullname, 'rb') as rfp:
            binData = rfp.read()
        fname = os.path.basename(fullname)
        fsize = os.path.getsize(fullname)
        height = width = int(math.sqrt(fsize))
        avgVal, maxVal, minVal = getImageDetails(rawFile)
        now = datetime.datetime.now()
        upDate = now.strftime('%Y-%m-%d')
        upUser = USER_NAME
        sql = "INSERT INTO rawImage_TBL2(raw_id , raw_height , raw_width"
        sql += ", raw_fname , raw_update , raw_uploader, raw_avg, raw_min, raw_max , raw_data) "
        sql += " VALUES(NULL," + str(height) + "," + str(width) + ",'"
        sql += fname + "','" + upDate + "','" + upUser + "'," + str(avgVal) + " , "
        sql += str(minVal) + ", " + str(maxVal) + ", "
        sql += " %s )"
        tupleData = (binData,)
        cur.execute(sql, tupleData)
        con.commit()
        cur.close()
        con.close()



#####################
#### 메인 코드부 ####
#####################
if __name__ == "__main__":
    window = Tk() # 윈도우 생성
    window.geometry("500x500") # 가로 500px, 세로 500px
    window.title("컴퓨터 비전(딥러닝 기법) ver 0.03")

    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="파일", menu=fileMenu)
    fileMenu.add_command(label="RAW 이미지 일괄 저장(DB)", command=uploadRawImage)
    fileMenu.add_command(label="RAW 이미지 일괄 저장(DB) + (평균, 최대값, 최소값)", command=uploadDetailRawImage)

    window.mainloop()