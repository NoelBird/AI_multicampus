from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import time
import pymysql
# 파일을 선택해서 메모리로 로딩하는 함수

###################################################################
# 전역변수 설정
###################################################################
IP_ADDR = '192.168.56.109'; USER_NAME = 'root'; USER_PASS = '1234'
DB_NAME = 'BigData_DB'; CHAR_SET = 'utf8'



####################
# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w, initValue=0) :
    retMemory= []
    for _ in range(h) :
        tmpList = []
        for _ in range(w) :
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory


# 파일을 메모리로 로딩하는 함수
def loadImageColor(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    inImage = []
    photo = Image.open(fname) # PIL 객체
    inW = photo.width; inH=photo.height
    ## 메모리 확보
    for _ in range(3) :
        inImage.append(malloc(inH, inW))

    photoRGB = photo.convert('RGB')
    for i in range(inH) :
        for k in range(inW) :
            r, g, b = photoRGB.getpixel((k,i))
            inImage[R][i][k] = r
            inImage[G][i][k] = g
            inImage[B][i][k] = b

def openImageColor() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return
    loadImageColor(filename)
    equalImageColor()

    displayImageColor()

def displayImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    VIEW_X = outW;    VIEW_Y = outH;   step = 1

    window.geometry(str(int(VIEW_X*1.2)) + 'x' + str(int(VIEW_Y*1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_X // 2, VIEW_Y // 2), image=paper, state='normal')

    import numpy
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0,outH, step) :
        tmpStr = ''
        for k in numpy.arange(0,outW, step) :
            i = int(i); k = int(k)
            r , g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.pack(expand=1, anchor=CENTER)
    canvas.bind('<Button-1>', mouseClickColor)
    canvas.bind('<ButtonRelease-1>', mouseDropColor)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

def saveImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # if outImage == None :
    #     return
    # saveFp = asksaveasfile(parent=window, mode='wb',
    #                        defaultextension='*.jpg', filetypes=(("JPG 파일", "*.jpg"), ("모든 파일", "*.*")))
    # if saveFp == '' or saveFp == None:
    #     return
    # outImage.save(saveFp.name)
    # print('Save~')

###############################################
##### 컴퓨터 비전(영상처리) 알고리즘 함수 모음 #####
###############################################
# 동일영상 알고리즘
def  equalImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][i][k] = inImage[RGB][i][k]
    #############################
    displayImageColor()


def addImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    value = askinteger("밝게/어둡게", "값-->", minvalue=-255, maxvalue=255)
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                if inImage[RGB][i][k] + value > 255 :
                    outImage[RGB][i][k] = 255
                elif inImage[RGB][i][k] + value < 0 :
                    outImage[RGB][i][k] = 0
                else :
                    outImage[RGB][i][k] = inImage[RGB][i][k] + value
    #############################
    displayImageColor()

def revImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = 255 - inImage[RGB][i][k]
    #############################
    displayImageColor()



# 이진화 알고리즘
def  bwImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    ## 영상의 평균 구하기.
    sum = []
    for RGB in range(3):
        sum.append(0)
        for i in range(inH) :
            for k in range(inW) :
                sum[RGB] += inImage[RGB][i][k]
    avg = [s // (inW * inH) for s in sum]

    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                if inImage[RGB][i][k] > avg[RGB] :
                    outImage[RGB][i][k] = 255
                else :
                    outImage[RGB][i][k] = 0

    displayImageColor()

def paraImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###\
    LUT = [0 for _ in range(256)]
    for input in range(256):
        LUT[input] = int(255 - 255 * math.pow(input / 128 - 1, 2))

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = LUT[inImage[RGB][i][k]]
    #############################
    displayImageColor()

def morphImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                               filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename2 == '' or filename2 == None:
        return
    inImage2 = []
    photo2 = Image.open(filename2) # PIL 객체
    inW2 = photo2.width; inH2=photo2.height
    ## 메모리 확보
    for _ in range(3) :
        inImage2.append(malloc(inH2, inW2))

    photoRGB2 = photo2.convert('RGB')
    for i in range(inH2) :
        for k in range(inW2) :
            r, g, b = photoRGB2.getpixel((k,i))
            inImage2[R][i][k] = r
            inImage2[G][i][k] = g
            inImage2[B][i][k] = b

    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    import threading
    import time
    def morpFunc():
        w1 = 1;
        w2 = 0
        for _ in range(20):
            for RGB in range(3) :
                for i in range(inH):
                    for k in range(inW):
                        newValue = int(inImage[RGB][i][k] * w1 + inImage2[RGB][i][k] * w2)
                        if newValue > 255:
                            newValue = 255
                        elif newValue < 0:
                            newValue = 0
                        outImage[RGB][i][k] = newValue
            displayImageColor()
            w1 -= 0.05;
            w2 += 0.05
            time.sleep(0.5)

    threading.Thread(target=morpFunc).start()


# 상하반전 알고리즘
def  upDownImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][inH-i-1][k] = inImage[RGB][i][k]

    displayImageColor()

# 영상 축소 알고리즘
def  zoomOutImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH//scale;  outW = inW//scale;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                outImage[RGB][i][k] = inImage[RGB][i*scale][k*scale]

    displayImageColor()

# 영상 확대 알고리즘
def  zoomInImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH*scale;  outW = inW*scale;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                outImage[RGB][i][k] = inImage[RGB][i//scale][k//scale]

    displayImageColor()




# 영상 축소 알고리즘 (평균변환)
def  zoomOutImage2Color() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH//scale;  outW = inW//scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][i//scale][k//scale] += inImage[RGB][i][k]
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] //= (scale*scale)

    displayImageColor()


# 영상 확대 알고리즘 (양선형 보간)
def  zoomInImage2Color() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH*scale;  outW = inW*scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    rH, rW, iH, iW = [0] * 4 # 실수위치 및 정수위치
    x, y = 0, 0 # 실수와 정수의 차이값
    C1,C2,C3,C4 = [0] * 4 # 결정할 위치(N)의 상하좌우 픽셀
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                rH = i / scale ; rW = k / scale
                iH = int(rH) ;  iW = int(rW)
                x = rW - iW; y = rH - iH
                if 0 <= iH < inH-1 and 0 <= iW < inW-1 :
                    C1 = inImage[RGB][iH][iW]
                    C2 = inImage[RGB][iH][iW+1]
                    C3 = inImage[RGB][iH+1][iW+1]
                    C4 = inImage[RGB][iH+1][iW]
                    newValue = C1*(1-y)*(1-x) + C2*(1-y)* x+ C3*y*x + C4*y*(1-x)
                    outImage[RGB][i][k] = int(newValue)

    displayImageColor()



# 영상 회전 알고리즘
def  rotateImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                xs = i ; ys = k;
                xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
                yd = int(math.sin(radian) * xs + math.cos(radian) * ys)
                if 0<= xd < inH and 0 <= yd < inW :
                    outImage[RGB][xd][yd] = inImage[RGB][i][k]

    displayImageColor()



# 영상 회전 알고리즘 - 중심, 역방향
def  rotateImage2Color() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    cx = inW//2; cy = inH//2
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                xs = i ; ys = k;
                xd = int(math.cos(radian) * (xs-cx) - math.sin(radian) * (ys-cy)) + cx
                yd = int(math.sin(radian) * (xs-cx) + math.cos(radian) * (ys-cy)) + cy
                if 0<= xd < outH and 0 <= yd < outW :
                    outImage[RGB][xs][ys] = inImage[RGB][xd][yd]
                else :
                    outImage[RGB][xs][ys] = 255

    displayImageColor()


## 엠보싱 처리
def  embossImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]
    ## 임시 입력영상 메모리 확보
    tmpInImage = []
    tmpOutImage = []
    for _ in range(3):
        tmpInImage.append(malloc(inH + MSIZE - 1, inW + MSIZE - 1, 127))
        tmpOutImage.append(malloc(outH, outW))
    ## 원 입력 --> 임시 입력
    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                tmpInImage[RGB][i+MSIZE//2][k+MSIZE//2] = inImage[RGB][i][k]
        ## 회선연산
        for i in range(MSIZE//2, inH + MSIZE//2) :
            for k in range(MSIZE//2, inW + MSIZE//2) :
                # 각 점을 처리.
                S = 0.0
                for m in range(0, MSIZE) :
                    for n in range(0, MSIZE) :
                        S += mask[m][n]*tmpInImage[RGB][i+m-MSIZE//2][k+n-MSIZE//2]
                tmpOutImage[RGB][i-MSIZE//2][k-MSIZE//2] = S
        ## 127 더하기 (선택)
        for i in range(outH) :
            for k in range(outW) :
                tmpOutImage[RGB][i][k] += 127
        ## 임시 출력 --> 원 출력
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage[RGB][i][k]
                if value > 255 :
                    value = 255
                elif value < 0 :
                    value = 0
                outImage[RGB][i][k] = int(value)

    displayImageColor()


# 히스토그램
import matplotlib.pyplot as plt
def  histoImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    inCountList = [[0] * 256 for _ in range(3)]
    outCountList = [[0] * 256 for _ in range(3)]

    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                inCountList[RGB][inImage[RGB][i][k]] += 1
        for i in range(outH) :
            for k in range(outW) :
                outCountList[RGB][outImage[RGB][i][k]] += 1

    plt.plot(inCountList[R], "r-")
    plt.plot(inCountList[G], "g-")
    plt.plot(inCountList[B], "b-")
    plt.legend(["R", "G", "B"])
    plt.show()


def  histoImage2Color() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outCountList = [[0] * 256 for _ in range(3)]
    normalCountList = [[0] * 256 for _ in range(3)]
    # 빈도수 계산
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                outCountList[RGB][outImage[RGB][i][k]] += 1
        maxVal = max(outCountList[RGB]); minVal = min(outCountList[RGB])
        High = 256
        # 정규화 = (카운트값 - 최소값) * High / (최대값 - 최소값)
        for i in range(len(outCountList[RGB])) :
            normalCountList[RGB][i] = (outCountList[RGB][i] - minVal) * High  / (maxVal-minVal)

    ## 서브 윈도창 생성 후 출력
    subWindow = Toplevel(window)
    subWindow.geometry('%dx%d' % (256*3, 256))
    subCanvas = Canvas(subWindow, width=256*3, height=256)
    subPaper = PhotoImage(width=256*3, height=256)
    subCanvas.create_image((256*3 // 2, 256 // 2), image=subPaper, state='normal')
    for RGB in range(3):
        for i in range(len(normalCountList[RGB])) :
            for k in range(int(normalCountList[RGB][i])) :
                # data= 0
                # dataWhite = 255
                if RGB == R:
                    subPaper.put('#d62719', (256*RGB + i, 255-k))
                elif RGB == G:
                    subPaper.put('#4fc34e', (256*RGB + i, 255-k))
                elif RGB == B:
                    subPaper.put('#1948b4', (256*RGB + i, 255-k))
    subCanvas.pack(expand=1, anchor=CENTER)
    subWindow.mainloop()



# 스트레칭 알고리즘
def  stretchImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3):
        maxVal = minVal = inImage[RGB][0][0]
        for i in range(inH) :
            for k in range(inW) :
                if inImage[RGB][i][k] < minVal :
                    minVal = inImage[RGB][i][k]
                elif inImage[RGB][i][k] > maxVal :
                    maxVal = inImage[RGB][i][k]
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][i][k] = int(((inImage[RGB][i][k] - minVal) / (maxVal - minVal)) * 255)

    displayImageColor()



# 스트레칭 알고리즘
def  endinImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    minAdd = askinteger("최소", "최소에서추가-->", minvalue=0, maxvalue=255)
    maxAdd = askinteger("최대", "최대에서감소-->", minvalue=0, maxvalue=255)
    for RGB in range(3):
        maxVal = minVal = inImage[RGB][0][0]
        for i in range(inH) :
            for k in range(inW) :
                if inImage[RGB][i][k] < minVal :
                    minVal = inImage[RGB][i][k]
                elif inImage[RGB][i][k] > maxVal :
                    maxVal = inImage[RGB][i][k]

        minVal += minAdd
        maxVal -= maxAdd

        for i in range(inH) :
            for k in range(inW) :
                value = int(((inImage[RGB][i][k] - minVal) / (maxVal - minVal)) * 255)
                if value < 0 :
                    value = 0
                elif value > 255 :
                    value = 255
                outImage[RGB][i][k] = value

    displayImageColor()



# 평활화 알고리즘
def  equalizeImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3):
        histo = [0] * 256; sumHisto = [0]*256; normalHisto = [0] * 256
        ## 히스토그램
        for i in range(inH) :
            for k in range(inW) :
                histo[inImage[RGB][i][k]] += 1
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
                outImage[RGB][i][k] = normalHisto[inImage[RGB][i][k]]
    displayImageColor()


# 화면이동 알고리즘
def moveImageColor() :
    global panYN
    panYN = True
    canvas.configure(cursor='mouse')


def mouseClickColor(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx,sy,ex,ey, panYN
    if panYN == False :
        return
    sx = event.x; sy = event.y


def mouseDropColor(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, panYN
    if panYN == False :
        return
    ex = event.x;    ey = event.y
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    mx = sx - ex; my = sy - ey
    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                if  0 <= i-my < outW and 0 <= k-mx < outH :
                    outImage[RGB][i-my][k-mx] = inImage[RGB][i][k]
    panYN = False
    displayImageColor()


#
# ## 임시 경로에 outImage를 저장하기.
# import random
# import struct
# def saveTempImage() :
#     global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
#     import tempfile
#     saveFp = tempfile.gettempdir() + "/" + str(random.randint(10000, 99999)) + ".raw"
#     if saveFp == '' or saveFp == None :
#         return
#     print(saveFp)
#     saveFp = open(saveFp, mode='wb')
#     for i in range(outH) :
#         for k in range(outW) :
#             for RGB in range(3):
#                 saveFp.write(struct.pack('B', outImage[RGB][i][k]))
#     saveFp.close()
#     return saveFp
#
#
# def findStatColor(fname) :
#     # 파일 열고, 읽기.
#     fsize = os.path.getsize(fname) # 파일의 크기(바이트)
#     inH = inW = int(math.sqrt(fsize)) # 핵심 코드
#     ## 입력영상 메모리 확보 ##
#     inImage = []
#     outImage = []
#     avg = []
#     maxVal = []
#     minVal = []
#     for _ in range(3):
#         inImage.append(malloc(inH, inH))
#     # 파일 --> 메모리
#     with open(fname, 'rb') as rFp:
#         for i in range(inH) :
#             for k in range(inW) :
#                 for RGB in range(3):
#                     inImage[RGB][i][k] = int(ord(rFp.read(1)))
#     for RGB in range(3):
#         sum = 0
#         for i in range(inH) :
#             for k in range(inW) :
#                 sum += inImage[RGB][i][k]
#         avg.append(sum // (inW * inH))
#         maxVal.append(inImage[RGB][0][0])
#         minVal.append(inImage[RGB][0][0])
#         for i in range(inH):
#             for k in range(inW):
#                 if inImage[RGB][i][k] < minVal[RGB]:
#                     minVal[RGB] = inImage[RGB][i][k]
#                 elif inImage[RGB][i][k] > maxVal[RGB]:
#                     maxVal[RGB] = inImage[RGB][i][k]
#     return avg, maxVal, minVal
#
#
# def saveMysqlColor() :
#     global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
#     con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
#                           db=DB_NAME, charset=CHAR_SET)
#     cur = con.cursor()
#
#     try:
#         sql = '''
#                 CREATE TABLE rawImage_TBL (
#                 raw_id INT AUTO_INCREMENT PRIMARY KEY,
#                 raw_fname VARCHAR(30),
#                 raw_extname CHAR(5),
#                 raw_height SMALLINT, raw_width SMALLINT,
#                 raw_avgR  TINYINT UNSIGNED ,
#                 raw_avgG  TINYINT UNSIGNED ,
#                 raw_avgB  TINYINT UNSIGNED ,
#                 raw_maxR  TINYINT UNSIGNED,
#                 raw_maxG  TINYINT UNSIGNED,
#                 raw_maxB  TINYINT UNSIGNED,
#                 raw_minR  TINYINT UNSIGNED,
#                 raw_minG  TINYINT UNSIGNED,
#                 raw_minB  TINYINT UNSIGNED,
#                 raw_dataR LONGBLOB,
#                 raw_dataG LONGBLOB,
#                 raw_dataB LONGBLOB);
#             '''
#         cur.execute(sql)
#     except:
#         pass
#
#     ## outImage를 임시 폴더에 저장하고, 이걸 fullname으로 전달.
#     fullname = saveTempImage()
#     fullname = fullname.name
#     with open(fullname, 'rb') as rfp:
#         binData = rfp.read()
#     for i in range(0, len(binData), 3):
#         binDataR = binData[i+R]
#         binDataG = binData[i+G]
#         binDataB = binData[i+B]
#
#     fname, extname = os.path.basename(fullname).split(".")
#     fsize = os.path.getsize(fullname)
#     height = width = int(math.sqrt(fsize))
#     avgVal, maxVal, minVal = findStatColor(fullname)  # 평균,최대,최소
#     avgValR, avgValG, avgValB = avgVal
#     maxValR, maxValG, maxValB = maxVal
#     minValR, minValG, minValB = minVal
#     sql = "INSERT INTO rawImage_TBL(raw_id , raw_fname,raw_extname,"
#     sql += "raw_height,raw_width,raw_avg,raw_max,raw_min,raw_data) "
#     sql += " VALUES(NULL,'" + fname + "','" + extname + "',"
#     sql += str(height) + "," + str(width) + ","
#     sql += str(avgValR) + "," + str(avgValG) + "," + str(avgValB) + ","
#     sql += str(maxValR) + "," + str(maxValG) + "," + str(maxValB) + ","
#     sql += str(minValR) + "," + str(minValG) + "," + str(minValB) + ","
#     sql += "%s, %s, %s )"
#     tupleData = (binDataR,binDataG, binDataB)
#     cur.execute(sql, tupleData)
#     con.commit()
#     cur.close()
#     con.close()
#     os.remove(fullname)
#     print("업로드 OK -->" + fullname)
#
#
# def loadMysqlColor() :
#     global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
#     con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
#                           db=DB_NAME, charset=CHAR_SET)
#     cur = con.cursor()
#     sql = "SELECT raw_id, raw_fname, raw_extname, raw_height, raw_width "
#     sql += "FROM rawImage_TBL"
#     cur.execute(sql)
#
#     queryList = cur.fetchall()
#     rowList = [ ':'.join(map(str,row)) for row in queryList]
#     import tempfile
#     def selectRecord( ) :
#         global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
#         selIndex = listbox.curselection()[0]
#         subWindow.destroy()
#         raw_id = queryList[selIndex][0]
#         sql = "SELECT raw_fname, raw_extname, raw_data FROM rawImage_TBL "
#         sql += "WHERE raw_id = " + str(raw_id)
#         cur.execute(sql)
#         fname, extname, binData = cur.fetchone()
#
#         fullPath = tempfile.gettempdir() + '/' + fname + "." + extname
#         with open(fullPath, 'wb') as wfp:
#             wfp.write(binData)
#         cur.close()
#         con.close()
#
#         loadImage(fullPath)
#         equalImage()
#
#     ## 서브 윈도에 목록 출력하기.
#     subWindow = Toplevel(window)
#     listbox = Listbox(subWindow)
#     button = Button(subWindow, text='선택', command = selectRecord)
#
#     for rowStr in rowList :
#         listbox.insert(END, rowStr)
#
#     listbox.pack(expand=1, anchor=CENTER)
#     button.pack()
#     subWindow.mainloop()
#
#
#     cur.close()
#     con.close()
####################
#### 전역변수 선언부 ####
####################
R, G, B = 0, 1, 2
inImage, outImage = [], []  # 3차원 리스트(배열)
inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)
####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝) ver 0.01")

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

## 마우스 이벤트

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImageColor)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImagePIL)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="덧셈/뺄셈", command=addImageColor)
comVisionMenu1.add_command(label="반전하기", command=revImageColor)
comVisionMenu1.add_command(label="파라볼라", command=paraImageColor)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="모핑", command=morphImageColor)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="통계", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화", command=bwImageColor)
comVisionMenu2.add_command(label="축소(평균변환)", command=zoomOutImage2Color)
comVisionMenu2.add_command(label="확대(양선형보간)", command=zoomInImage2Color)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label="히스토그램", command=histoImageColor)
comVisionMenu2.add_command(label="히스토그램(내꺼)", command=histoImage2Color)
comVisionMenu2.add_command(label="명암대비", command=stretchImageColor)
comVisionMenu2.add_command(label="End-In탐색", command=endinImageColor)
comVisionMenu2.add_command(label="평활화", command=equalizeImageColor)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전", command=upDownImageColor)
comVisionMenu3.add_command(label="이동", command=moveImageColor)
comVisionMenu3.add_command(label="축소", command=zoomOutImageColor)
comVisionMenu3.add_command(label="확대", command=zoomInImageColor)
comVisionMenu3.add_command(label="회전1", command=rotateImageColor)
comVisionMenu3.add_command(label="회전2(중심,역방향)", command=rotateImage2Color)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="화소영역 처리", menu=comVisionMenu4)
comVisionMenu4.add_command(label="엠보싱", command=embossImageColor)

# comVisionMenu5 = Menu(mainMenu)
# mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
# comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysqlColor)
# comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMysqlColor)
# comVisionMenu5.add_separator()
# comVisionMenu5.add_command(label="CSV 열기", command=openCSV)
# comVisionMenu5.add_command(label="CSV로 저장", command=saveCSV)
# comVisionMenu5.add_separator()
# comVisionMenu5.add_command(label="엑셀 열기", command=openExcel)
# comVisionMenu5.add_command(label="엑셀로 저장", command=saveExcel)
# comVisionMenu5.add_command(label="엑셀 아트로 저장", command=saveExcelArt)


window.mainloop()