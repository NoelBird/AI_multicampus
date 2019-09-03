from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import numpy as np
####################
#### 함수 선언부 ####
####################
# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w, initValue=0, dataType=np.uint8) :
    retMemory = np.zeros((h, w), dtype=dataType)
    retMemory += initValue
    return retMemory


# 파일을 메모리로 로딩하는 함수
def loadImage(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = os.path.getsize(fname) # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize)) # 핵심 코드
    ## 입력영상 메모리 확보 ##
    inImage = np.fromfile(fname, dtype=np.uint8)
    inImage = inImage.reshape(inH, inW)

# 파일을 선택해서 메모리로 로딩하는 함수
import time
def openImage() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if not filename:
        return
    # start = time.time()
    loadImage(filename)
    equalImage()
    # print(time.time()-start)


import struct
def saveImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb',
                       defaultextension='*.raw',
                       filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if not saveFp:
        return
    saveFp.write(outImage.tobytes())
    saveFp.close()


def displayImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global VIEW_X, VIEW_Y
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()

    ## 고정된 화면 크기
    if outH <= VIEW_Y or outW <= VIEW_X :
        VIEW_X = outW
        VIEW_Y = outH
        step = 1
    else :
        VIEW_X = 512
        VIEW_Y = 512
        step = outW / VIEW_X

    window.geometry(str(int(VIEW_Y*1.2)) + 'x' + str(int(VIEW_X*1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    rgbStr = ''  # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, step):
        tmpStr = ''
        for k in numpy.arange(0, outW, step):
            i = int(i);
            k = int(k)
            r = g = b = int(outImage[i][k])
            tmpStr += ' #%02x%02x%02x' % (r, g, b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.bind('<Button-1>', mouseClick)
    canvas.bind('<ButtonRelease-1>', mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

###############################################
##### 컴퓨터 비전(영상처리) 알고리즘 함수 모음 #####
###############################################
# 동일영상 알고리즘
def  equalImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    outImage = inImage[:]

    displayImage()

# 동일영상 알고리즘
def  addImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    value = askinteger("밝게/어둡게", "값-->", minvalue=-255, maxvalue=255)
    start = time.time()
    inImage = inImage.astype(np.int16)
    outImage = inImage + value
    # 조건으로 범위 지정
    outImage = np.where(outImage > 255, 255, outImage)
    outImage = np.where(outImage < 0, 0, outImage)

    seconds = time.time() - start
    displayImage()
    status.configure(text=status.cget("text") + "\t\t 시간(초):"
                          + "{0:.2f}".format(seconds))

# 반전영상 알고리즘
def  revImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    # outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    outImage = 255 - inImage
    # for i in range(inH) :
    #     for k in range(inW) :
    #         outImage[i][k] = 255 - inImage[i][k]
    displayImage()


# 이진화 알고리즘
def  bwImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = inImage.copy[:]
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    ## 영상의 평균 구하기.
    avg = inImage.mean()

    outImage = np.where(inImage > avg, 255, 0)

    displayImage()


# 파라볼라 알고리즘 with LUT
def  paraImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = inImage[:]
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    x = np.array([i for i in range(0, 256)])
    LUT = 255 - 255*np.power(x/128 - 1, 2)
    LUT = LUT.astype(np.uint8)
    outImage = LUT[inImage]
    displayImage()


# 상하반전 알고리즘
def  upDownImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = inImage[:]
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    outImage = inImage[::-1, :]
    displayImage()

# 화면이동 알고리즘
def moveImage() :
    global panYN
    panYN = True
    canvas.configure(cursor='mouse')

def mouseClick(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx,sy,ex,ey, panYN
    if panYN == False :
        return
    sx = event.x; sy = event.y


#TODO: from here
def mouseDrop(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, panYN
    if panYN == False :
        return
    ex = event.x;    ey = event.y
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = np.zeros_like(inImage)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    mx = sx - ex; my = sy - ey
    if mx < 0 and my < 0:
        outImage[-mx:inH, -my:inW] = inImage[0:inH+mx, 0:inW+my]

    outImage = np.zeros_like(inImage)


    # outImage[outIdxH, outIdxW] = inImage[]

    # print(outIdxW)
    # print(len(outIdxH))
    # print(len(idxH[:len(outIdxH)]))
    #
    # outImage[outIdxH][outIdxW] = inImage[idxH[:len(outIdxH)]][idxW[:len(outIdxW)]]
    # if  0 <= i-my < outW and 0 <= k-mx < outH :
    panYN = False
    displayImage()


# 영상 축소 알고리즘
def  zoomOutImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH//scale;  outW = inW//scale;
    ###### 메모리 할당 ################
    outImage = inImage[:]
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    outImage = inImage[::scale, ::scale]

    displayImage()


# 영상 축소 알고리즘 (평균변환)
def  zoomOutImage2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH//scale;  outW = inW//scale;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    mxx, myy = np.mgrid[range(inH), range(inW)]
    outImage[(mxx // scale, myy // scale)] += inImage[(mxx, myy)].copy()

    # mxx, myy = np.mgrid[range(outH), range(outW)]
    # outImage[mxx, myy] //= (scale)
    # important: trying to reshape image will create complete 4-dimensional compy

    displayImage()

# 영상 확대 알고리즘
def  zoomInImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH*scale;  outW = inW*scale;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    mxx, myy = np.mgrid[range(outH), range(outW)]
    outImage[mxx, myy] = inImage[mxx//scale, myy//scale]

    displayImage()

# 영상 확대 알고리즘 (양선형 보간)
def  zoomInImage2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH*scale;  outW = inW*scale;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    rH, rW, iH, iW = [0] * 4 # 실수위치 및 정수위치
    x, y = 0, 0 # 실수와 정수의 차이값
    C1,C2,C3,C4 = [0] * 4 # 결정할 위치(N)의 상하좌우 픽셀
    mxx, myy = np.mgrid[range(outH), range(outW)]
    rH, iH = np.mgrid[range(outH), range(outW)]
    rH //= scale
    # rH = rH.astype(np.uint8)
    iH //= scale
    # iH = iH.astype(np.uint8)
    x = rW - iW
    y = rH - iH

    try:
        C1 = inImage[iH, iW]
        # C1 = inImage[iH[0 <= iH < inH - 1], iW[0 <= iW < inW-1]]
        C2 = inImage[iH, iW+1]
        C3 = inImage[iH+1, iW+1]
        C4 = inImage[iH+1, iW]
    except:
        pass
    newValue = C1*(1-y)*(1-x) + C2*(1-y)* x+ C3*y*x + C4*y*(1-x)
    outImage[mxx, myy] = newValue.astype(np.uint8)

    displayImage()

#TODO: to here


# 영상 회전 알고리즘
def  rotateImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = np.zeros_like(inImage)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    xs_lin = np.arange(inH)
    xs = np.repeat(xs_lin, inW)
    ys_lin = np.arange(inW)
    ys = np.repeat(ys_lin, inH)
    xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
    yd = int(math.sin(radian) * xs + math.cos(radian) * ys)
    outImage[xd[0<= xd < inH]][yd[0 <= yd < inW]] = inImage[xs_lin[0<= xd < inH]][ys_lin[0 <= yd < inW]]

    displayImage()

# 영상 회전 알고리즘 - 중심, 역방향
def  rotateImage2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    cx = inW//2; cy = inH//2
    for i in range(outH) :
        for k in range(outW) :
            xs = i ; ys = k;
            xd = int(math.cos(radian) * (xs-cx) - math.sin(radian) * (ys-cy)) + cx
            yd = int(math.sin(radian) * (xs-cx) + math.cos(radian) * (ys-cy)) + cy
            if 0<= xd < outH and 0 <= yd < outW :
                outImage[xs][ys] = inImage[xd][yd]
            else :
                outImage[xs][ys] = 255

    displayImage()


# 히스토그램
import matplotlib.pyplot as plt
def  histoImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    inCountList = np.arange(256)
    outCountList = [0] * 256

    for i in range(outH) :
        for k in range(outW) :
            outCountList[outImage[i][k]] += 1

    plt.plot(inCountList)
    plt.plot(outCountList)
    plt.show()

def  histoImage2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outCountList = [0] * 256
    normalCountList = [0] * 256
    # 빈도수 계산
    for i in range(outH) :
        for k in range(outW) :
            outCountList[outImage[i][k]] += 1
    maxVal = max(outCountList); minVal = min(outCountList)
    High = 256
    # 정규화 = (카운트값 - 최소값) * High / (최대값 - 최소값)
    for i in range(len(outCountList)) :
        normalCountList[i] = (outCountList[i] - minVal) * High  / (maxVal-minVal)
    ## 서브 윈도창 생성 후 출력
    subWindow = Toplevel(window)
    subWindow.geometry('256x256')
    subCanvas = Canvas(subWindow, width=256, height=256)
    subPaper = PhotoImage(width=256, height=256)
    subCanvas.create_image((256//2, 256//2), image=subPaper, state='normal')

    for i in range(len(normalCountList)) :
        for k in range(int(normalCountList[i])) :
            data= 0
            subPaper.put('#%02x%02x%02x' % (data, data, data), (i, 255-k))
    subCanvas.pack(expand=1, anchor=CENTER)
    subWindow.mainloop()


# 스트레칭 알고리즘
def  stretchImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    maxVal = minVal = inImage[0][0]
    for i in range(inH) :
        for k in range(inW) :
            if inImage[i][k] < minVal :
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal :
                maxVal = inImage[i][k]
    for i in range(inH) :
        for k in range(inW) :
            outImage[i][k] = int(((inImage[i][k] - minVal) / (maxVal - minVal)) * 255)

    displayImage()


# 스트레칭 알고리즘
def  endinImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    maxVal = minVal = inImage[0][0]
    for i in range(inH) :
        for k in range(inW) :
            if inImage[i][k] < minVal :
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal :
                maxVal = inImage[i][k]

    minAdd = askinteger("최소", "최소에서추가-->", minvalue=0, maxvalue=255)
    maxAdd = askinteger("최대", "최대에서감소-->", minvalue=0, maxvalue=255)
    #
    minVal += minAdd
    maxVal -= maxAdd

    for i in range(inH) :
        for k in range(inW) :
            value = int(((inImage[i][k] - minVal) / (maxVal - minVal)) * 255)
            if value < 0 :
                value = 0
            elif value > 255 :
                value = 255
            outImage[i][k] = value

    displayImage()


# 평활화 알고리즘
def  equalizeImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    histo = [0] * 256; sumHisto = [0]*256; normalHisto = [0] * 256
    ## 히스토그램
    for i in range(inH) :
        for k in range(inW) :
            histo[inImage[i][k]] += 1
    ## 누적히스토그램
    sValue = 0
    for i in range(len(histo)) :
        sValue += histo[i]
        sumHisto[i] = sValue
    ## 정규화 누적 히스토그램
    for i in range(len(sumHisto)):
        normalHisto[i] = int(sumHisto[i] / (inW*inH) * 255)
    ## 영상처리
    for i in range(inH) :
        for k in range(inW) :
            outImage[i][k] = normalHisto[inImage[i][k]]
    displayImage()

## 엠보싱 처리
def  embossImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]
    ## 임시 입력영상 메모리 확보
    tmpInImage = malloc(inH+MSIZE-1, inW+MSIZE-1, 127)
    tmpOutImage = malloc(outH, outW)
    ## 원 입력 --> 임시 입력
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+MSIZE//2][k+MSIZE//2] = inImage[i][k]
    ## 회선연산
    for i in range(MSIZE//2, inH + MSIZE//2) :
        for k in range(MSIZE//2, inW + MSIZE//2) :
            # 각 점을 처리.
            S = 0.0
            for m in range(0, MSIZE) :
                for n in range(0, MSIZE) :
                    S += mask[m][n]*tmpInImage[i+m-MSIZE//2][k+n-MSIZE//2]
            tmpOutImage[i-MSIZE//2][k-MSIZE//2] = S
    ## 127 더하기 (선택)
    for i in range(outH) :
        for k in range(outW) :
            tmpOutImage[i][k] += 127
    ## 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            value = tmpOutImage[i][k]
            if value > 255 :
                value = 255
            elif value < 0 :
                value = 0
            outImage[i][k] = int(value)

    displayImage()

# 모핑 알고리즘
def  morphImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ## 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if filename2 == '' or filename2 == None:
        return

    fsize = os.path.getsize(filename2)  # 파일의 크기(바이트)
    inH2 = inW2 = int(math.sqrt(fsize))  # 핵심 코드
    ## 입력영상 메모리 확보 ##
    # 파일 --> 메모리
    inImage2 = np.fromfile(filename2, dtype=np.uint8)
    inImage2 = inImage2.reshape(inH2, inW2)
    ###### 메모리 할당 ################
    outImage = inImage[:]
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    #w1 = askinteger("원영상 가중치", "가중치(%)->", minvalue=0, maxvalue=100)
    #w2 = 1- (w1/100);    w1 = 1-w2

    import threading
    import time
    def morpFunc() :
        global outImage
        w1 = 1;
        w2 = 0
        for _ in range(20):
            outImage = inImage*w1 + inImage2*w2
            outImage = np.where(outImage > 255, 255, outImage)
            outImage = np.where(outImage < 0, 0, outImage)
            displayImage()
            w1 -= 0.05;        w2 += 0.05
            time.sleep(0.5)
    threading.Thread(target=morpFunc).start()


## 임시 경로에 outImage를 저장하기.
import random
def saveTempImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    import tempfile
    saveFp = tempfile.gettempdir() + "/" + str(random.randint(10000, 99999)) + ".raw"
    if saveFp == '' or saveFp == None :
        return
    print(saveFp)
    saveFp = open(saveFp, mode='wb')
    for i in range(outH) :
        for k in range(outW) :
            saveFp.write(struct.pack('B', outImage[i][k]))
    saveFp.close()
    return saveFp


def findStat(fname) :
    # 파일 열고, 읽기.
    fsize = os.path.getsize(fname) # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize)) # 핵심 코드
    ## 입력영상 메모리 확보 ##
    # 파일 --> 메모리
    inImage = np.fromfile(fname, dtype=np.uint8)
    inImage = inImage.reshape(inH, inW)
    avg = inImage.mean()
    minVal = np.min(inImage)
    maxVal = np.max(inImage)
    return avg, maxVal, minVal

import pymysql
IP_ADDR = '192.168.56.106'; USER_NAME = 'root'; USER_PASS = '1234'
DB_NAME = 'BigData_DB'; CHAR_SET = 'utf8'
def saveMysql() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    try:
        sql = '''
                CREATE TABLE rawImage_TBL (
                raw_id INT AUTO_INCREMENT PRIMARY KEY,
                raw_fname VARCHAR(30),
                raw_extname CHAR(5),
                raw_height SMALLINT, raw_width SMALLINT,
                raw_avg  TINYINT UNSIGNED , 
                raw_max  TINYINT UNSIGNED,  raw_min  TINYINT UNSIGNED,
                raw_data LONGBLOB);
            '''
        cur.execute(sql)
    except:
        pass

    ## outImage를 임시 폴더에 저장하고, 이걸 fullname으로 전달.
    fullname = saveTempImage()
    fullname = fullname.name
    with open(fullname, 'rb') as rfp:
        binData = rfp.read()

    fname, extname = os.path.basename(fullname).split(".")
    fsize = os.path.getsize(fullname)
    height = width = int(math.sqrt(fsize))
    avgVal, maxVal, minValue = findStat(fullname)  # 평균,최대,최소
    sql = "INSERT INTO rawImage_TBL(raw_id , raw_fname,raw_extname,"
    sql += "raw_height,raw_width,raw_avg,raw_max,raw_min,raw_data) "
    sql += " VALUES(NULL,'" + fname + "','" + extname + "',"
    sql += str(height) + "," + str(width) + ","
    sql += str(avgVal) + "," + str(maxVal) + "," + str(minValue)
    sql += ", %s )"
    tupleData = (binData,)
    cur.execute(sql, tupleData)
    con.commit()
    cur.close()
    con.close()
    os.remove(fullname)
    print("업로드 OK -->" + fullname)


def loadMysql() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    sql = "SELECT raw_id, raw_fname, raw_extname, raw_height, raw_width "
    sql += "FROM rawImage_TBL"
    cur.execute(sql)

    queryList = cur.fetchall()
    rowList = [ ':'.join(map(str,row)) for row in queryList]
    import tempfile
    def selectRecord( ) :
        global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
        selIndex = listbox.curselection()[0]
        subWindow.destroy()
        raw_id = queryList[selIndex][0]
        sql = "SELECT raw_fname, raw_extname, raw_data FROM rawImage_TBL "
        sql += "WHERE raw_id = " + str(raw_id)
        cur.execute(sql)
        fname, extname, binData = cur.fetchone()

        fullPath = tempfile.gettempdir() + '/' + fname + "." + extname
        with open(fullPath, 'wb') as wfp:
            wfp.write(binData)
        cur.close()
        con.close()

        loadImage(fullPath)
        equalImage()

    ## 서브 윈도에 목록 출력하기.
    subWindow = Toplevel(window)
    listbox = Listbox(subWindow)
    button = Button(subWindow, text='선택', command = selectRecord)

    for rowStr in rowList :
        listbox.insert(END, rowStr)

    listbox.pack(expand=1, anchor=CENTER)
    button.pack()
    subWindow.mainloop()


    cur.close()
    con.close()

# 파일을 메모리로 로딩하는 함수
def loadCSV(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = 0
    fp = open(fname,'r')
    for _ in fp :
        fsize += 1
    inH = inW = int(math.sqrt(fsize)) # 핵심 코드
    fp.close()
    ## 입력영상 메모리 확보 ##
    inImage=[]
    inImage=malloc(inH,inW)
    # 파일 --> 메모리
    with open(fname, 'r') as rFp:
        for row_list in rFp :
            row, col, value = list(map(int,row_list.strip().split(',')))
            inImage[row][col] = value

# 파일을 선택해서 메모리로 로딩하는 함수
def openCSV() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return
    loadCSV(filename)
    equalImage()

import csv
def saveCSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='*.csv', filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    with open(saveFp.name,'w', newline='') as wFp :
        csvWriter = csv.writer(wFp)
        for i in range(outH):
            for k in range(outW):
                row_list = [i, k, outImage[i][k]]
                csvWriter.writerow(row_list)
    print('CSV. save OK~')


import xlwt
def saveExcel() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='*.xls', filetypes=(("XLS 파일", "*.xls"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    xlsName = saveFp.name
    sheetName = os.path.basename(filename)
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheetName)

    for i in range(outH) :
        for k in range(outW) :
            ws.write(i, k, outImage[i][k])

    wb.save(xlsName)
    print('Excel. save OK~')

import xlsxwriter
def saveExcelArt() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='*.xls', filetypes=(("XLS 파일", "*.xls"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    xlsName = saveFp.name
    sheetName = os.path.basename(filename)

    wb = xlsxwriter.Workbook(xlsName)
    ws = wb.add_worksheet(sheetName)

    ws.set_column(0, outW-1, 1.0) # 약 0.34
    for i in range(outH) :
        ws.set_row(i, 9.5) # 약 0.35

    for i in range(outH) :
        for k in range(outW) :
            data = outImage[i][k]
            # data 값으로 셀의 배경색을 조절 #000000 ~ #FFFFFF
            if data > 15 :
                hexStr = '#' + hex(data)[2:] * 3
            else :
                hexStr = '#' + ('0' + hex(data)[2:]) * 3
            # 셀의 포맷을 준비
            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)
            ws.write(i, k, '', cell_format)

    wb.close()
    print('Excel Art. save OK~')

def openExcel():
    pass
####################
#### 전역변수 선언부 ####
####################
inImage, outImage = [], [] ; inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
panYN = False
sx,sy,ex,ey = [0] * 4
VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)
####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(Numpy) ver 0.08")

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

## 마우스 이벤트


mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImage)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImage)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="덧셈/뺄셈", command=addImage)
comVisionMenu1.add_command(label="반전하기", command=revImage)
comVisionMenu1.add_command(label="파라볼라", command=paraImage)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="모핑", command=morphImage)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="통계", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화", command=bwImage)
comVisionMenu2.add_command(label="축소(평균변환)", command=zoomOutImage2)
comVisionMenu2.add_command(label="확대(양선형보간)", command=zoomInImage2)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label="히스토그램", command=histoImage)
comVisionMenu2.add_command(label="히스토그램(내꺼)", command=histoImage2)
comVisionMenu2.add_command(label="명암대비", command=stretchImage)
comVisionMenu2.add_command(label="End-In탐색", command=endinImage)
comVisionMenu2.add_command(label="평활화", command=equalizeImage)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전", command=upDownImage)
comVisionMenu3.add_command(label="이동", command=moveImage)
comVisionMenu3.add_command(label="축소", command=zoomOutImage)
comVisionMenu3.add_command(label="축소2(평균이용)", command=zoomOutImage2)
comVisionMenu3.add_command(label="확대", command=zoomInImage)
comVisionMenu3.add_command(label="회전1", command=rotateImage)
comVisionMenu3.add_command(label="회전2(중심,역방향)", command=rotateImage2)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="화소영역 처리", menu=comVisionMenu4)
comVisionMenu4.add_command(label="엠보싱", command=embossImage)

comVisionMenu5 = Menu(mainMenu)
mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysql)
comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMysql)
comVisionMenu5.add_separator()
comVisionMenu5.add_command(label="CSV 열기", command=openCSV)
comVisionMenu5.add_command(label="CSV로 저장", command=saveCSV)
comVisionMenu5.add_separator()
comVisionMenu5.add_command(label="엑셀 열기", command=openExcel)
comVisionMenu5.add_command(label="엑셀로 저장", command=saveExcel)
comVisionMenu5.add_command(label="엑셀 아트로 저장", command=saveExcelArt)

window.mainloop()