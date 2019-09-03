import tkinter
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import numpy as np
import struct
import matplotlib.pyplot as plt
import threading
import time
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import colorsys

import random
import tempfile
import pymysql
import csv


#######################
#### 클래스 선언부 ####
#######################
class Window(tkinter.Tk): # tkinter Tk를 상속
    def __init__(self, H=500, W=500):
        super(Window, self).__init__()
        self.canvas = None
        self.inImage = None
        self.outImage = None
        self.photo = None

        self.H = H
        self.W = W

        self.panYN = N
        self.viewX = W
        self.viewY = H

        self.sx = 0
        self.sy = 0
        self.ex = W-1
        self.ey = H-1

    def putSize(self, H: int, W: int):
        self.H = H
        self.W = W

    def getSize(self):
        return self.H, self.W


class Canvas(tkinter.Canvas): # tkinter Canvas를 상속
    def __init__(self, window, height=500, width=500):
        super(Canvas, self).__init__(window, height=height, width=width)
        self.paper = None
        self.H, self.W = window.getSize()

    def putSize(self, H: int, W: int):
        self.H = H
        self.W = W

    def getSize(self):
        return self.H, self.W


class Paper:
    def __init__(self, window: Canvas):
        self.paper = None
        self.H, self.W = window.getSize()

    def putSize(self, H: int, W: int):
        self.H = H
        self.W = W

    def getSize(self):
        return self.H, self.W


class __Image:
    def __init__(self, H=-1, W=-1):
        self.H = H
        self.W = W
        self.filename = ''
        self.mem = None

    def putSize(self, H: int, W: int):
        self.H = H
        self.W = W

    def getSize(self):
        return self.H, self.W

    def malloc(self, initValue: int = 0) -> list:
        """
        이미지의 높이, 폭 값을 받아온 다음 메모리를 할당하여 list로 돌려준다.
        :param initValue:
        :return:
        """
        if self.H == -1 or self.W == -1:
            print("set H and W!! @ %s" % __class__)
            exit(-1)

        retMemory = []
        for RGB in range(3):
            retMemory.append([])
            for i in range(self.H):
                retMemory[RGB].append([])
                for k in range(self.W):
                    retMemory[RGB][i].append(initValue)
        self.mem = retMemory


class InImage(__Image):
    def __init__(self, H=-1, W=-1):
        super(InImage, self).__init__(H=H, W=W)


class OutImage(__Image):
    def __init__(self, H=-1, W=-1):
        super(OutImage, self).__init__(H=H, W=W)



#########################
#### 전역변수 선언부 ####
#########################
# image information
# mywin = MyWindow(H=500, W=500)
#
# mycan = MyCanvas(parent=mywin)
# mywin.canvas = mycan
#
# mypap = MyPaper(parent=mycan)
# mycan.paper = mypap
#
# inImage = InImage()
# outImage = OutImage()

# DB information
IP_ADDR = '192.168.56.106'
USER_NAME = 'root'
USER_PASS = '1234'
DB_NAME = 'BigData_DB'
CHAR_SET = 'utf8'

# tkinter wrapping variables
BOTTOM = tkinter.BOTTOM
X = tkinter.X
SUNKEN = tkinter.SUNKEN
W = tkinter.W

# tkinter wrapping Classes
Label = tkinter.Label
Menu = tkinter.Menu

# color information
R = 0
G = 1
B = 2


#####################
#### 함수 선언부 ####
#####################
def loadImage(window, fname: str) -> None:
    photo = Image.open(fname)  # PIL 객체
    image = InImage()

    ## 메모리 확보
    inW = photo.width
    inH = photo.height

    image.putSize(H=inH, W=inW)
    image.malloc()

    photoRGB = photo.convert('RGB')
    for i in range(inH):
        for k in range(inW):
            r, g, b = photoRGB.getpixel((k, i))
            image.mem[R][i][k] = r
            image.mem[G][i][k] = g
            image.mem[B][i][k] = b

    window.photo = photo
    return image


# 파일을 선택해서 메모리로 로딩하는 함수
def openImageColor(window):
    filename = askopenfilename(parent=window,
                               filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if not filename:
        return
    window.inImage = loadImage(window, filename)
    equalImage(window)


def saveImageColor(window):
    outImage = window.outImage
    if not outImage:
        return
    outArray= []
    for i in range(outImage.H):
        tmpList = []
        for k in range(outImage.W):
            tup = tuple([outImage.mem[R][i][k], outImage.mem[G][i][k], outImage.mem[B][i][k],])
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), 'RGB')

    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='.', filetypes=(("그림 파일", "*.png;*.jpg;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if not saveFp:
        return
    savePhoto.save(saveFp.name)
    print('Save~')



def displayImageColor(window):
    canvas = window.canvas
    outImage = window.outImage
    if canvas:  # 예전에 실행한 적이 있다.
        canvas.destroy()

    window.viewY, window.viewX = outImage.getSize() # H, W값 순서
    step = 1

    window.geometry(str(int(window.viewX * 1.2)) + 'x' + str(int(window.viewY * 1.2)))  # 벽
    canvas = Canvas(window, height=window.viewY, width=window.viewX)
    window.canvas = canvas

    paper = PhotoImage(height=window.viewY, width=window.viewX)
    canvas.paper = paper

    canvas.create_image(
        (window.viewX // 2, window.viewY // 2), image=paper, state='normal')

    ## 성능 개선
    rgbStr = ''  # 전체 픽셀의 문자열을 저장
    for i in np.arange(0, outImage.H, step):
        tmpStr = ''
        for k in np.arange(0, outImage.W, step):
            i = int(i)
            k = int(k)
            r, g, b = outImage.mem[R][i][k], outImage.mem[G][i][k], outImage.mem[B][i][k]
            tmpStr += ' #%02x%02x%02x' % (r, g, b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    # canvas.bind('<Button-1>', mouseClick)
    # canvas.bind('<ButtonRelease-1>', mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)
    # status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))


# ###############################################
# ##### 컴퓨터 비전(영상처리) 알고리즘 함수 모음 #####
# ###############################################
# # 동일영상 알고리즘
def equalImage(window):
    inImage = window.inImage
    outImage = window.outImage
    ###### 메모리 할당 ################
    outH, outW = inImage.getSize()
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3):
        for i in range(inImage.H):
            for k in range(inImage.W):
                outImage.mem[RGB][i][k] = inImage.mem[RGB][i][k]

    window.outImage = outImage

    displayImageColor(window)


def addImageColor(window):
    ## 중요! 코드. 출력영상 크기 결정 ##
    inImage = window.inImage
    outH = inImage.H
    outW = inImage.W
    ## 메모리 확보
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    value = askinteger("밝게/어둡게", "값-->", minvalue=-255, maxvalue=255)
    for RGB in range(3) :
        for i in range(inImage.H) :
            for k in range(inImage.W) :
                if inImage.mem[RGB][i][k] + value > 255 :
                    outImage.mem[RGB][i][k] = 255
                elif inImage.mem[RGB][i][k] + value < 0 :
                    outImage.mem[RGB][i][k] = 0
                else :
                    outImage.mem[RGB][i][k] = inImage.mem[RGB][i][k] + value
    #############################

    window.outImage = outImage
    displayImageColor(window)


def revImageColor(window):
    ## 중요! 코드. 출력영상 크기 결정 ##
    inImage = window.inImage
    outH = inImage.H
    outW = inImage.W
    ## 메모리 확보
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    for RGB in range(3):
        for i in range(inImage.H):
            for k in range(inImage.W):
                outImage.mem[RGB][i][k] = 255 - inImage.mem[RGB][i][k]
    #############################
    window.outImage = outImage
    displayImageColor(window)


def paraImageColor(window):
    ## 중요! 코드. 출력영상 크기 결정 ##
    inImage = window.inImage
    outH = inImage.H
    outW = inImage.W
    ## 메모리 확보
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###\
    LUT = [0 for _ in range(256)]
    for input in range(256):
        LUT[input] = int(255 - 255 * math.pow(input / 128 - 1, 2))

    for RGB in range(3):
        for i in range(inImage.H):
            for k in range(inImage.W):
                outImage.mem[RGB][i][k] = LUT[inImage.mem[RGB][i][k]]
    #############################
    window.outImage = outImage
    displayImageColor(window)


def morphImageColor(window):
    ## 중요! 코드. 출력영상 크기 결정 ##
    inImage = window.inImage
    outH = inImage.H
    outW = inImage.W
    ## 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                               filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if not filename2:
        return
    inImage2 = loadImage(window, filename2)

    ## 메모리 확보
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()

    # 작은 쪽에 맞춤
    if inImage.H > inImage2.H:
        inImage.H = inImage2.H
    if inImage.W > inImage2.W:
        inImage.W = inImage2.W

    import threading
    import time

    def morpFunc():
        w1 = 1
        w2 = 0
        for _ in range(20):
            for RGB in range(3) :
                for i in range(inImage.H):
                    for k in range(inImage.W):
                        newValue = int(inImage.mem[RGB][i][k] * w1 + inImage2.mem[RGB][i][k] * w2)
                        if newValue > 255:
                            newValue = 255
                        elif newValue < 0:
                            newValue = 0
                        outImage.mem[RGB][i][k] = newValue
            window.outImage = outImage
            displayImageColor(window)
            w1 -= 0.05;
            w2 += 0.05
            time.sleep(0.5)

    threading.Thread(target=morpFunc).start()


def addSValuePillow(window):
    photo = window.photo
    inImage = window.inImage
    ## 중요! 코드. 출력영상 크기 결정 ##
    value = askfloat("","0~1~10")
    photo2 = photo.copy()
    photo2 = ImageEnhance.Color(photo2)
    photo2 = photo2.enhance(value)

    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inImage.H
    outW = inImage.W
    ###### 메모리 할당 ################
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()

    ## 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            r, g, b = photo2.getpixel((k, i))
            outImage.mem[R][i][k] = r
            outImage.mem[G][i][k] = g
            outImage.mem[B][i][k] = b

    displayImageColor(window)


def addSValueHSV(window):
    ## 입력 RGB --> 입력 HSV
    # 메모리 확보
    inImage = window.inImage
    inH = inImage.H
    inW = inImage.W
    inImageHSV = InImage(H=inImage.H, W=inImage.W)
    inImageHSV.malloc()
    # RGB -> HSV
    for i in range(inH):
        for k in range(inW):
            r, g, b = inImage.mem[R][i][k], inImage.mem[G][i][k], inImage.mem[B][i][k]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            inImageHSV.mem[0][i][k], inImageHSV.mem[1][i][k], inImageHSV.mem[2][i][k] = h, s, v

    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    ###### 메모리 할당 ################
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    value = askfloat("", "-255~255") # -255 ~ 255
    value /= 255
    ## HSV --> RGB
    for i in range(outH):
        for k in range(outW):
            newS = inImageHSV.mem[1][i][k] + value
            if newS < 0 :
                newS = 0
            elif newS > 1.0 :
                newS = 1.0
            h, s, v = inImageHSV.mem[0][i][k], newS, inImageHSV.mem[2][i][k]*255
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            outImage.mem[R][i][k], outImage.mem[G][i][k], outImage.mem[B][i][k] = int(r), int(g), int(b)

    window.outImage = outImage
    displayImageColor(window)


# 이진화 알고리즘
def bwImage(window):
    ## 중요! 코드. 출력영상 크기 결정 ##
    inImage = window.inImage
    outH = inImage.H
    outW = inImage.W
    ###### 메모리 할당 ################
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    ## 영상의 평균 구하기.
    sumList = []
    for RGB in range(3):
        sumList.append(0)
        for i in range(inImage.H):
            for k in range(inImage.W):
                sumList[RGB] += inImage.mem[RGB][i][k]
    avg = [s // (inImage.W * inImage.H) for s in sumList]

    for i in range(inImage.H):
        for k in range(inImage.W):
            avgVal = int(sum([inImage.mem[tmp][i][k] for tmp in range(3)]) / 3)
            if avgVal > avg[RGB]:
                newVal = 255
            else:
                newVal = 0
            for RGB in range(3):
                outImage.mem[RGB][i][k] = newVal

    window.outImage = outImage
    displayImageColor(window)


# 영상 축소 알고리즘 (평균변환)
def zoomOutImage2Color(window):
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    inImage = window.inImage
    ## 중요! 코드. 출력영상 크기 결정 ##

    outH = inImage.H//scale
    outW = inImage.W//scale
    ###### 메모리 할당 ################
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3):
        for i in range(inImage.H):
            for k in range(inImage.W):
                outImage.mem[RGB][i//scale][k//scale] += inImage.mem[RGB][i][k]
        for i in range(outImage.H):
            for k in range(outImage.W):
                outImage.mem[RGB][i][k] //= (scale*scale)

    window.outImage = outImage
    displayImageColor(window)


# 영상 확대 알고리즘 (양선형 보간)
def zoomInImage2Color(window):
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    inImage = window.inImage
    inH = inImage.H
    inW = inImage.W
    outH = inImage.H*scale
    outW = inImage.W*scale
    ###### 메모리 할당 ################
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    rH, rW, iH, iW = [0] * 4 # 실수위치 및 정수위치
    x, y = 0, 0 # 실수와 정수의 차이값
    C1,C2,C3,C4 = [0] * 4 # 결정할 위치(N)의 상하좌우 픽셀
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                rH = i / scale
                rW = k / scale
                iH = int(rH)
                iW = int(rW)
                x = rW - iW
                y = rH - iH
                if 0 <= iH < inH-1 and 0 <= iW < inW-1 :
                    C1 = inImage.mem[RGB][iH][iW]
                    C2 = inImage.mem[RGB][iH][iW+1]
                    C3 = inImage.mem[RGB][iH+1][iW+1]
                    C4 = inImage.mem[RGB][iH+1][iW]
                    newValue = C1*(1-y)*(1-x) + C2*(1-y)* x+ C3*y*x + C4*y*(1-x)
                    outImage.mem[RGB][i][k] = int(newValue)

    window.outImage = outImage
    displayImageColor(window)


# 영상 회전 알고리즘
def rotateImageColor(window):
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    inImage = window.inImage
    outH = inImage.H
    outW = inImage.W
    ###### 메모리 할당 ################
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    for RGB in range(3):
        for i in range(inImage.H):
            for k in range(inImage.W):
                xs = i
                ys = k
                xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
                yd = int(math.sin(radian) * xs + math.cos(radian) * ys)
                if 0 <= xd < inImage.H and 0 <= yd < inImage.W:
                    outImage.mem[RGB][xd][yd] = inImage.mem[RGB][i][k]

    window.outImage = outImage
    displayImageColor(window)


# 영상 회전 알고리즘 - 중심, 역방향
def rotateImage2Color(window):
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    inImage = window.inImage
    inH = inImage.H
    inW = inImage.W
    outH = inImage.H
    outW = inImage.W
    ###### 메모리 할당 ################
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    cx = inW//2
    cy = inH//2
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                xs = i
                ys = k
                xd = int(math.cos(radian) * (xs-cx) - math.sin(radian) * (ys-cy)) + cx
                yd = int(math.sin(radian) * (xs-cx) + math.cos(radian) * (ys-cy)) + cy
                if 0 <= xd < outH and 0 <= yd < outW:
                    outImage.mem[RGB][xs][ys] = inImage.mem[RGB][xd][yd]
                else:
                    outImage.mem[RGB][xs][ys] = 255

    window.outImage = outImage
    displayImageColor(window)


## 엠보싱 처리
def embossImageRGB(window):
    ## 중요! 코드. 출력영상 크기 결정 ##
    inImage = window.inImage
    inH = inImage.H
    inW = inImage.W
    outH = inImage.H
    outW = inImage.W
    ###### 메모리 할당 ################
    outImage = OutImage(H=outH, W=outW)
    outImage.malloc()
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]
    ## 임시 입력영상 메모리 확보
    tmpInImage = InImage(H=inH + MSIZE - 1, W=inW + MSIZE - 1)
    tmpInImage.malloc(initValue=127)

    tmpOutImage = OutImage(H=outH, W=outW)
    tmpOutImage.malloc()

    ## 원 입력 --> 임시 입력
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                tmpInImage.mem[RGB][i+MSIZE//2][k+MSIZE//2] = inImage.mem[RGB][i][k]
        ## 회선연산
        for i in range(MSIZE//2, inH + MSIZE//2):
            for k in range(MSIZE//2, inW + MSIZE//2):
                # 각 점을 처리.
                S = 0.0
                for m in range(0, MSIZE):
                    for n in range(0, MSIZE):
                        S += mask[m][n]*tmpInImage.mem[RGB][i+m-MSIZE//2][k+n-MSIZE//2]
                tmpOutImage.mem[RGB][i-MSIZE//2][k-MSIZE//2] = S
        ## 127 더하기 (선택)
        for i in range(outH):
            for k in range(outW):
                tmpOutImage.mem[RGB][i][k] += 127
        ## 임시 출력 --> 원 출력
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage.mem[RGB][i][k]
                if value > 255 :
                    value = 255
                elif value < 0 :
                    value = 0
                outImage.mem[RGB][i][k] = int(value)

    window.outImage = outImage
    displayImageColor(window)
####################
#### 메인 코드부 ###
####################
if __name__ == "__main__":
    win = Window(H=500, W=500)
    win.geometry("500x500")
    win.title("컴퓨터 비전(딥러닝 기법) ver 0.04")

    can = Canvas(win)
    win.canvas = can

    pap = Paper(can)
    can.paper = pap

    inImage = InImage()
    win.inImage = inImage

    outImage = OutImage()
    win.outImage = outImage

    status = Label(win, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
    status.pack(side=BOTTOM, fill=X)

    mainMenu = Menu(win)
    win.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="파일", menu=fileMenu)
    fileMenu.add_command(label="파일 열기", command=lambda: openImageColor(win))
    fileMenu.add_separator()
    fileMenu.add_command(label="파일 저장", command=lambda: saveImageColor(win))

    comVisionMenu1 = Menu(mainMenu)
    mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
    comVisionMenu1.add_command(label="덧셈/뺄셈", command=lambda: addImageColor(win))
    comVisionMenu1.add_command(label="반전하기", command=lambda: revImageColor(win))
    comVisionMenu1.add_command(label="파라볼라", command=lambda: paraImageColor(win))
    comVisionMenu1.add_separator()
    comVisionMenu1.add_command(label="모핑", command=lambda: morphImageColor(win))
    comVisionMenu1.add_separator()
    comVisionMenu1.add_command(label="채도조절(Pillow)", command=lambda: addSValuePillow(win))
    comVisionMenu1.add_command(label="채도조절(HSV)", command=lambda: addSValueHSV(win))

    comVisionMenu2 = Menu(mainMenu)
    mainMenu.add_cascade(label="통계", menu=comVisionMenu2)
    comVisionMenu2.add_command(label="이진화", command=lambda: bwImage(win))
    comVisionMenu2.add_command(label="축소(평균변환)", command=lambda: zoomOutImage2Color(win))
    comVisionMenu2.add_command(label="확대(양선형보간)", command=lambda: zoomInImage2Color(win))
    comVisionMenu2.add_separator()
    # comVisionMenu2.add_command(label="히스토그램", command=histoImage)
    # comVisionMenu2.add_command(label="히스토그램(내꺼)", command=histoImage2)
    # comVisionMenu2.add_command(label="명암대비", command=stretchImage)
    # comVisionMenu2.add_command(label="End-In탐색", command=endinImage)
    # comVisionMenu2.add_command(label="평활화", command=equalizeImage)

    comVisionMenu3 = Menu(mainMenu)
    mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
    # comVisionMenu3.add_command(label="상하반전", command=upDownImageColor)
    # comVisionMenu3.add_command(label="이동", command=moveImage)
    # comVisionMenu3.add_command(label="축소", command=zoomOutImageColor)
    # comVisionMenu3.add_command(label="확대", command=zoomInImageColor)
    comVisionMenu3.add_command(label="회전1", command=lambda: rotateImageColor(win))
    comVisionMenu3.add_command(label="회전2(중심,역방향)", command=lambda: rotateImage2Color(win))

    comVisionMenu4 = Menu(mainMenu)
    mainMenu.add_cascade(label="화소영역 처리", menu=comVisionMenu4)
    comVisionMenu4.add_command(label="엠보싱(RGB)", command=lambda: embossImageRGB(win))
    # comVisionMenu4.add_command(label="엠보싱(Pillow제공)", command=embossImagePillow)
    # comVisionMenu4.add_command(label="엠보싱(HSV)", command=embossImageHSV)
    # comVisionMenu4.add_separator()
    # comVisionMenu4.add_command(label="블러링(RGB)", command=blurrImageRGB)

    #
    # comVisionMenu5 = Menu(mainMenu)
    # mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
    # comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysql)
    # comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMysql)
    # comVisionMenu5.add_separator()
    # comVisionMenu5.add_command(label="CSV 열기", command=openCSV)
    # comVisionMenu5.add_command(label="CSV로 저장", command=saveCSV)
    # comVisionMenu5.add_separator()
    # comVisionMenu5.add_command(label="엑셀 열기", command=openExcel)
    # comVisionMenu5.add_command(label="엑셀로 저장", command=saveExcel)
    # comVisionMenu5.add_command(label="엑셀 아트로 저장", command=saveExcelArt)

    win.mainloop()
