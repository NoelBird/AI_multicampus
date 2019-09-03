from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import time
import cv2
# 파일을 선택해서 메모리로 로딩하는 함수

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
def loadImageColor(fnameOrCvData) : # 파일명 or OpenCV 개체
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    inImage = []
    #################################
    ## PIL 개체 --> OpenCV 개체로 복사
    if type(fnameOrCvData) == str :
        cvData = cv2.imread(fnameOrCvData)  # 파일-->CV데이터
    else :
        cvData = fnameOrCvData
    cvPhoto = cv2.cvtColor(cvData, cv2.COLOR_BGR2RGB) # 중요! CV개체
    photo = Image.fromarray(cvPhoto)  # 중요! PIL 객체
    inW = photo.width;    inH = photo.height
    ################################
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
    global VIEW_X, VIEW_Y
    # VIEW_X, VIEW_Y = 512, 512
    ## 고정된 화면 크기
    # 가로/세로 비율 계산
    ratio = outH / outW
    if ratio < 1:
        VIEW_X = int(512 * ratio)
    else:
        VIEW_X = 512
    if ratio > 1:
        VIEW_Y = int(512 * ratio)
    else:
        VIEW_Y = 512

    if outH <= VIEW_X :
        VIEW_X = outH; stepX = 1
    if outH > VIEW_X :
        if ratio < 1 :
            VIEW_X = int(512 * ratio)
        else :
            VIEW_X = 512
        stepX = outH / VIEW_X

    if outW <= VIEW_Y:
        VIEW_Y = outW; stepY = 1
    if outW > VIEW_Y:
        if ratio > 1 :
            VIEW_Y = int(512 * ratio)
        else :
            VIEW_Y = 512

        stepY = outW / VIEW_Y

    window.geometry(str(int(VIEW_Y*1.2)) + 'x' + str(int(VIEW_X*1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_X, width=VIEW_Y)
    paper = PhotoImage(height=VIEW_X, width=VIEW_Y)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0,outH, stepX) :
        tmpStr = ''
        for k in numpy.arange(0,outW, stepY) :
            i = int(i); k = int(k)
            r , g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

import numpy as np
def saveImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if outImage == None :
        return
    outArray= []
    for i in range(outH) :
        tmpList = []
        for k in range(outW) :
            tup = tuple([outImage[R][i][k],outImage[G][i][k],outImage[B][i][k],])
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), 'RGB')

    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='.', filetypes=(("그림 파일", "*.png;*.jpg;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    savePhoto.save(saveFp.name)
    print('Save~')

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

    # 작은 쪽에 맞춤
    if inH > inH2 :
        inH = inH2
    if inW > inW2 :
        inW = inW2
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


def  embossImageRGB() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]
    ## 임시 입력영상 메모리 확보
    tmpInImage, tmpOutImage=[], []
    for _ in range(3):
        tmpInImage.append(malloc(inH+MSIZE-1, inW+MSIZE-1, 127))
    for _ in range(3):
        tmpOutImage.append(malloc(outH, outW))
    ## 원 입력 --> 임시 입력
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                tmpInImage[RGB][i+MSIZE//2][k+MSIZE//2] = inImage[RGB][i][k]
    ## 회선연산
    for RGB in range(3):
        for i in range(MSIZE//2, inH + MSIZE//2) :
            for k in range(MSIZE//2, inW + MSIZE//2) :
                # 각 점을 처리.
                S = 0.0
                for m in range(0, MSIZE) :
                    for n in range(0, MSIZE) :
                        S += mask[m][n]*tmpInImage[RGB][i+m-MSIZE//2][k+n-MSIZE//2]
                tmpOutImage[RGB][i-MSIZE//2][k-MSIZE//2] = S
    ## 127 더하기 (선택)
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                tmpOutImage[RGB][i][k] += 127
    ## 임시 출력 --> 원 출력
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage[RGB][i][k]
                if value > 255 :
                    value = 255
                elif value < 0 :
                    value = 0
                outImage[RGB][i][k] = int(value)

    displayImageColor()

def  embossImagePillow() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ## 중요! 코드. 출력영상 크기 결정 ##
    photo2 = photo.copy()
    photo2 = photo2.filter(ImageFilter.EMBOSS)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ## 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            r, g, b = photo2.getpixel((k, i))
            outImage[R][i][k] = r
            outImage[G][i][k] = g
            outImage[B][i][k] = b

    displayImageColor()

import colorsys
sx, sy, ex, ey = [0] * 4
def  embossImageHSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey
    ## 이벤트 바인드
    canvas.bind('<Button-3>', rightMouseClick_embossImageHSV)
    canvas.bind('<Button-1>', leftMouseClick)
    canvas.bind('<B1-Motion>', leftMouseMove)
    canvas.bind('<ButtonRelease-1>', leftMouseDrop_embossImageHSV)
    canvas.configure(cursor='mouse')

def leftMouseDrop_embossImageHSV(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey
    ex = event.x;    ey = event.y
    ##################
    print(inH, VIEW_X, inW, VIEW_Y)
    if inH > VIEW_X :
        sx = int(sx * (inH / VIEW_X)); ex = int(ex * (inH / VIEW_X))
    if inW > VIEW_Y :
        sy = int(sy * (inW / VIEW_Y)); ey = int(ey * (inW / VIEW_Y))

    # 마우스 클릭을 어떤 방향이든지 인정
    if sx > ex :
        sx, ex = ex, sx
    if sy > ey :
        sy, ey = ey, sy
    __embossImageHSV()
    ##################
    canvas.unbind('<Button-3>')
    canvas.unbind('<Button-1>')
    canvas.unbind('<B1-Motion>')
    canvas.unbind('<ButtonRelease-1>')

boxLine = None
def leftMouseMove(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, boxLine
    ex = event.x ; ey = event.y
    if not boxLine :
        pass
    else :
        canvas.delete(boxLine)
    boxLine = canvas.create_rectangle(sx, sy, ex, ey, fill=None)

def leftMouseClick(event) :
    global sx, sy, ex, ey
    sx = event.x; sy = event.y

def rightMouseClick_embossImageHSV(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey
    sx = 0; sy = 0; ey = inH-1; ex = inW-1
    ##################
    __embossImageHSV()
    ##################
    canvas.unbind('<Button-3>')
    canvas.unbind('<Button-1>')
    canvas.unbind('<B1-Motion>')
    canvas.unbind('<ButtonRelease-1>')

def  __embossImageHSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 입력 RGB --> 입력 HSV
    # 메모리 확보
    inImageHSV = [];
    for _ in range(3):
        inImageHSV.append(malloc(inH, inW))
    # RGB -> HSV
    for i in range(inH) :
        for k in range(inW) :
            r, g, b = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k] = h, s, v

    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [[-1, 0, 0],
            [0, 0, 0],
            [0, 0, 1]]
    ## 임시 입력영상 메모리 확보
    tmpInImageV, tmpOutImageV = [], []
    tmpInImageV=(malloc(inH + MSIZE - 1, inW + MSIZE - 1, 127))
    tmpOutImageV=(malloc(outH, outW))
    ## 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImageV[i + MSIZE // 2][k + MSIZE // 2] = inImageHSV[2][i][k]
    ## 회선연산
    for i in range(MSIZE // 2, inH + MSIZE // 2):
        for k in range(MSIZE // 2, inW + MSIZE // 2):
            # 각 점을 처리.
            S = 0.0
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImageV[i + m - MSIZE // 2][k + n - MSIZE // 2]
            tmpOutImageV[i - MSIZE // 2][k - MSIZE // 2] = S*255
    ## 127 더하기 (선택)
    for i in range(outH):
        for k in range(outW):
            tmpOutImageV[i][k] += 127
            if tmpOutImageV[i][k] > 255 :
                tmpOutImageV[i][k] = 255
            elif tmpOutImageV[i][k] < 0 :
                tmpOutImageV[i][k] = 0

    ## HSV --> RGB
    for i in range(outH):
        for k in range(outW):
            if sx <= k <= ex and sy <= i <= ey : # 범위에 포함되면
                h, s, v = inImageHSV[0][i][k], inImageHSV[1][i][k], tmpOutImageV[i][k]
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]= int(r), int(g), int(b)
            else :
                outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]

    displayImageColor()


def  blurrImageRGB() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [ [ 1/9, 1/9, 1/9],
             [ 1/9, 1/9, 1/9],
             [ 1/9, 1/9, 1/9] ]
    ## 임시 입력영상 메모리 확보
    tmpInImage, tmpOutImage=[], []
    for _ in range(3):
        tmpInImage.append(malloc(inH+MSIZE-1, inW+MSIZE-1, 127))
    for _ in range(3):
        tmpOutImage.append(malloc(outH, outW))
    ## 원 입력 --> 임시 입력
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                tmpInImage[RGB][i+MSIZE//2][k+MSIZE//2] = inImage[RGB][i][k]
    ## 회선연산
    for RGB in range(3):
        for i in range(MSIZE//2, inH + MSIZE//2) :
            for k in range(MSIZE//2, inW + MSIZE//2) :
                # 각 점을 처리.
                S = 0.0
                for m in range(0, MSIZE) :
                    for n in range(0, MSIZE) :
                        S += mask[m][n]*tmpInImage[RGB][i+m-MSIZE//2][k+n-MSIZE//2]
                tmpOutImage[RGB][i-MSIZE//2][k-MSIZE//2] = S
    ## 127 더하기 (선택)
    # for RGB in range(3):
    #     for i in range(outH) :
    #         for k in range(outW) :
    #             tmpOutImage[RGB][i][k] += 127
    ## 임시 출력 --> 원 출력
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage[RGB][i][k]
                if value > 255 :
                    value = 255
                elif value < 0 :
                    value = 0
                outImage[RGB][i][k] = int(value)

    displayImageColor()

def  addSValuePillow() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ## 중요! 코드. 출력영상 크기 결정 ##
    value = askfloat("","0~1~10")
    photo2 = photo.copy()
    photo2 = ImageEnhance.Color(photo2)
    photo2 = photo2.enhance(value)


    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ## 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            r, g, b = photo2.getpixel((k, i))
            outImage[R][i][k] = r
            outImage[G][i][k] = g
            outImage[B][i][k] = b

    displayImageColor()

def  addSValueHSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 입력 RGB --> 입력 HSV
    # 메모리 확보
    inImageHSV = [];
    for _ in range(3):
        inImageHSV.append(malloc(inH, inW))
    # RGB -> HSV
    for i in range(inH):
        for k in range(inW):
            r, g, b = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k] = h, s, v

    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    value = askfloat("", "-255~255") # -255 ~ 255
    value /= 255
    ## HSV --> RGB
    for i in range(outH):
        for k in range(outW):
            newS = inImageHSV[1][i][k] + value
            if newS < 0 :
                newS = 0
            elif newS > 1.0 :
                newS = 1.0
            h, s, v = inImageHSV[0][i][k], newS, inImageHSV[2][i][k]*255
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(b)

    displayImageColor()

###################################
## OpenCV 용 컴퓨터 비전/딥러닝
##################################
def toColorOutArray(pillowPhoto) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###### 메모리 할당 ################
    outH = pillowPhoto.height; outW = pillowPhoto.width
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    photoRGB = pillowPhoto.convert('RGB')
    for i in range(outH) :
        for k in range(outW) :
            r,g,b = photoRGB.getpixel((k,i))
            outImage[R][i][k],outImage[G][i][k],outImage[B][i][k]=r,g,b
    displayImageColor()


def embossOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None :
        return

    cvPhoto2 = cvPhoto[:]
    mask = np.zeros((3,3), np.float32)
    mask[0][0] = -1; mask[2][2] = 1;
    cvPhoto2=cv2.filter2D(cvPhoto2, -1, mask)
    cvPhoto2 += 127
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArray(photo2)

def greyscaleOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None :
        return
    ###이 부분이 OpenCV 처리 부분##########################
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def blurOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None :
        return
    ###이 부분이 OpenCV 처리 부분##########################
    mSize = askinteger("블러링", "마스크 크기:")
    cvPhoto2 = cvPhoto[:]
    mask = np.ones((mSize, mSize), np.float32) / (mSize*mSize)
    cvPhoto2 = cv2.filter2D(cvPhoto2, -1, mask)
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def rotateOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    angle = askinteger("회전", "각도:")
    cvPhoto2 = cvPhoto[:]
    rotate_matrix = cv2.getRotationMatrix2D((outH//2, outW//2), angle, 1) # 중앙점, 각도, 스케일
    cvPhoto2 = cv2.warpAffine(cvPhoto2, rotate_matrix, (outH, outW))
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def zoomInOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    scale = askfloat("확대/축소", "배수:")
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.resize(cvPhoto2, None, fx=scale, fy=scale)
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def waveHorOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    cvPhoto2 = np.zeros(cvPhoto.shape, dtype=cvPhoto.dtype)
    for i in range(inH) :
        for k in range(inW) :
            oy = int(15.0 * math.sin(2*3.14*k / 180))
            ox = 0
            if i+oy < inH :
                cvPhoto2[i][k] = cvPhoto [(i+oy) % inH][k]
            else :
                cvPhoto2[i][k] = 0
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)
def waveVirOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    cvPhoto2 = np.zeros(cvPhoto.shape, dtype=cvPhoto.dtype)
    for i in range(inH):
        for k in range(inW):
            ox = int(25.0 * math.sin(2 * 3.14 * i / 180))
            oy = 0
            if k + ox < inW:
                cvPhoto2[i][k] = cvPhoto[i][(k + ox) % inW]
            else:
                cvPhoto2[i][k] = 0
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def cartoonOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    cvPhoto2 = cv2.medianBlur(cvPhoto2, 7)
    edges = cv2.Laplacian(cvPhoto2, cv2.CV_8U, ksize=5)
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    cvPhoto2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def faceDetectOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(face_rects)
    for (x, y, w, h) in face_rects:
        cv2.rectangle(cvPhoto2, (x, y), (x + w, y + w), (0, 255, 0), 3)

    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def hanibalOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    faceMask = cv2.imread("C:/images/images(ML)/mask_hannibal.png")
    h_mask, w_mask = faceMask.shape[:2]
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    for (x, y, w, h) in face_rects:
        if h> 0 and w > 0 :
            x = int(x + 0.1*w); y = int(y+0.4*h)
            w = int(0.8 *w) ; h = int(0.8*h)
            cvPhoto2_2 = cvPhoto2[y:y+h, x:x+w]
            faceMask_small = cv2.resize(faceMask, (w,h), interpolation=cv2.INTER_AREA)
            grey_mask = cv2.cvtColor(faceMask_small, cv2.COLOR_RGB2GRAY)
            ret, mask = cv2.threshold(grey_mask, 50, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            maskedFace = cv2.bitwise_and(faceMask_small, faceMask_small, mask=mask)
            maskedFrame = cv2.bitwise_and(cvPhoto2_2, cvPhoto2_2,mask_inv)
            cvPhoto2[y:y+h, x:x+w] = cv2.add(maskedFace, maskedFrame)
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def catFaceDetectOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(face_rects)
    for (x, y, w, h) in face_rects:
        cv2.rectangle(cvPhoto2, (x, y), (x + w, y + w), (0, 255, 0), 3)

    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def catHanibalOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")
    faceMask = cv2.imread("C:/images/images(ML)/mask_hannibal.png")
    h_mask, w_mask = faceMask.shape[:2]
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    for (x, y, w, h) in face_rects:
        if h > 0 and w > 0:
            x = int(x + 0.1 * w);
            y = int(y + 0.4 * h)
            w = int(0.8 * w);
            h = int(0.8 * h)
            cvPhoto2_2 = cvPhoto2[y:y + h, x:x + w]
            faceMask_small = cv2.resize(faceMask, (w, h), interpolation=cv2.INTER_AREA)
            grey_mask = cv2.cvtColor(faceMask_small, cv2.COLOR_RGB2GRAY)
            ret, mask = cv2.threshold(grey_mask, 50, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            maskedFace = cv2.bitwise_and(faceMask_small, faceMask_small, mask=mask)
            maskedFrame = cv2.bitwise_and(cvPhoto2_2, cvPhoto2_2, mask_inv)
            cvPhoto2[y:y + h, x:x + w] = cv2.add(maskedFace, maskedFrame)
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def deepOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    cvPhoto2 = cvPhoto[:]
    ###########################
    CONF_VALUE = 0.2
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
    image = cvPhoto2
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > CONF_VALUE:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            cv2.rectangle(image, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    cvPhoto2 = image
    ############################
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArray(photo2)


def deep2OpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto, frame
    filename = askopenfilename(parent=window,
                               filetypes=(("동영상 파일", "*.mp4"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    cap = cv2.VideoCapture(filename)  # filename 대신에 0을 넣으면 카메라에서 바로 받아옴
    s_factor = 0.5 # 화면 크기 비율

    frameCount = 0
    while True:
        ret, frame = cap.read()  # 현재 한 장면
        if not ret:
            break
        frameCount += 1
        if frameCount % 8 == 0:  # 8은 화면 속도 조절. 실제로 다 하면, 너무 느릴 수 있어서 이렇게 하는 것임
            frame = cv2.resize(frame, None, fx=s_factor, fy=s_factor, interpolation=cv2.INTER_AREA)

            # frame = cvPhoto[:]
            ###########################
            CONF_VALUE = 0.2
            CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                "sofa", "train", "tvmonitor"]
            COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
            net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
            image = frame
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
            net.setInput(blob)
            detections = net.forward()
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > CONF_VALUE:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    cv2.rectangle(image, (startX, startY), (endX, endY),
                        COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(image, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            frame = image
            ############################
            cv2.imshow('Deep Learning', frame)
            c = cv2.waitKey(True)
            if c == 27:  # ESC키
                break
            elif c == ord('c') or c == ord('c'):
                captureVideo()
                window.update()
    cap.release()
    cv2.destroyAllWindows()


def captureVideo():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto, frame
    photo2 = Image.fromarray(frame)
    toColorOutArray(photo2)







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
window.title("컴퓨터 비전(OpenCV) ver 0.4")

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

## 마우스 이벤트

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImageColor)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImageColor)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="덧셈/뺄셈", command=addImageColor)
comVisionMenu1.add_command(label="반전하기", command=revImageColor)
comVisionMenu1.add_command(label="파라볼라", command=paraImageColor)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="모핑", command=morphImageColor)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="채도조절(Pillow)", command=addSValuePillow)
comVisionMenu1.add_command(label="채도조절(HSV)", command=addSValueHSV)

# comVisionMenu2 = Menu(mainMenu)
# mainMenu.add_cascade(label="통계", menu=comVisionMenu2)
# comVisionMenu2.add_command(label="이진화", command=bwImage)
# comVisionMenu2.add_command(label="축소(평균변환)", command=zoomOutImage2)
# comVisionMenu2.add_command(label="확대(양선형보간)", command=zoomInImage2)
# comVisionMenu2.add_separator()
# comVisionMenu2.add_command(label="히스토그램", command=histoImage)
# comVisionMenu2.add_command(label="히스토그램(내꺼)", command=histoImage2)
# comVisionMenu2.add_command(label="명암대비", command=stretchImage)
# comVisionMenu2.add_command(label="End-In탐색", command=endinImage)
# comVisionMenu2.add_command(label="평활화", command=equalizeImage)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전", command=upDownImageColor)
# comVisionMenu3.add_command(label="이동", command=moveImage)
comVisionMenu3.add_command(label="축소", command=zoomOutImageColor)
comVisionMenu3.add_command(label="확대", command=zoomInImageColor)
# comVisionMenu3.add_command(label="회전1", command=rotateImage)
# comVisionMenu3.add_command(label="회전2(중심,역방향)", command=rotateImage2)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="화소영역 처리", menu=comVisionMenu4)
comVisionMenu4.add_command(label="엠보싱(RGB)", command=embossImageRGB)
comVisionMenu4.add_command(label="엠보싱(Pillow제공)", command=embossImagePillow)
comVisionMenu4.add_command(label="엠보싱(HSV)", command=embossImageHSV)
comVisionMenu4.add_separator()
comVisionMenu4.add_command(label="블러링(RGB)", command=blurrImageRGB)

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

openCVMenu = Menu(mainMenu)
mainMenu.add_cascade(label="OpenCV 딥러닝", menu=openCVMenu)
openCVMenu.add_command(label="엠보싱(OpenCV)", command=embossOpenCV)
openCVMenu.add_command(label="그레이스케일(OpenCV)", command=greyscaleOpenCV)
openCVMenu.add_command(label="블러링(OpenCV)", command=blurOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="회전", command=rotateOpenCV)
openCVMenu.add_command(label="확대", command=zoomInOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="수평 웨이브", command=waveHorOpenCV)
openCVMenu.add_command(label="수직 웨이브", command=waveVirOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="카툰화", command=cartoonOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="얼굴인식(머신러닝)", command=faceDetectOpenCV)
openCVMenu.add_command(label="한니발 마스크(머신러닝)", command=hanibalOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="냥이 얼굴(머신러닝)", command=catFaceDetectOpenCV)
openCVMenu.add_command(label="냥이 마스크(머신러닝)", command=catHanibalOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="사물 인식(딥러닝) - 정지영상", command=deepOpenCV)
openCVMenu.add_command(label="사물 인식(딥러닝) - 동영상", command=deep2OpenCV)

window.mainloop()