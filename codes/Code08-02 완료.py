from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path

####################
#### 함수 선언부 ####
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
def loadImage(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = os.path.getsize(fname) # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize)) # 핵심 코드
    ## 입력영상 메모리 확보 ##
    inImage=[]
    inImage=malloc(inH,inW)
    # 파일 --> 메모리
    with open(filename, 'rb') as rFp:
        for i in range(inH) :
            for k in range(inW) :
                inImage[i][k] = int(ord(rFp.read(1)))

# 파일을 선택해서 메모리로 로딩하는 함수
def openImage() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return
    loadImage(filename)
    equalImage()

import struct
def saveImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb',
        defaultextension='*.raw', filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None :
        return
    for i in range(outH) :
        for k in range(outW) :
            saveFp.write(struct.pack('B', outImage[i][k]))
    saveFp.close()

def displayImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    ## 화면 크기를 조절
    window.geometry(str(outH) + 'x' + str(outW)) # 벽
    canvas = Canvas(window, height=outH, width=outW) # 보드
    paper = PhotoImage(height=outH, width=outW) # 빈 종이
    canvas.create_image((outH//2, outW//2), image=paper, state='normal')
    ## 출력영상 --> 화면에 한점씩 찍자.
    # for i in range(outH) :
    #     for k in range(outW) :
    #         r = g = b = outImage[i][k]
    #         paper.put("#%02x%02x%02x" % (r, g, b), (k, i))
    ## 성능 개선
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in range(outH) :
        tmpStr = ''
        for k in range(outW) :
            r = g = b = outImage[i][k]
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.bind('<Button-1>', mouseClick)
    canvas.bind('<ButtonRelease-1>', mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)

###############################################
##### 컴퓨터 비전(영상처리) 알고리즘 함수 모음 #####
###############################################
# 동일영상 알고리즘
def  equalImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(inH) :
        for k in range(inW) :
            outImage[i][k] = inImage[i][k]

    displayImage()

# 동일영상 알고리즘
def  addImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    value = askinteger("밝게/어둡게", "값-->", minvalue=-255, maxvalue=255)
    for i in range(inH) :
        for k in range(inW) :
            v = inImage[i][k] + value
            if v > 255 :
                v = 255
            elif v < 0 :
                v = 0
            outImage[i][k] = v

    displayImage()

# 반전영상 알고리즘
def  revImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(inH) :
        for k in range(inW) :
            outImage[i][k] = 255 - inImage[i][k]
    displayImage()

# 이진화 알고리즘
def  bwImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    ## 영상의 평균 구하기.
    sum = 0
    for i in range(inH) :
        for k in range(inW) :
            sum += inImage[i][k]
    avg = sum // (inW * inH)

    for i in range(inH) :
        for k in range(inW) :
            if inImage[i][k] > avg :
                outImage[i][k] = 255
            else :
                outImage[i][k] = 0

    displayImage()

# 파라볼라 알고리즘 with LUT
def  paraImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    LUT = [0 for _ in range(256)]
    for input in range(256) :
        LUT[input]  = int(255 - 255 * math.pow(input/128 -1, 2))

    for i in range(inH) :
        for k in range(inW) :
            input = inImage[i][k]
            outImage[i][k] = LUT[inImage[i][k]]
    displayImage()

# 상하반전 알고리즘
def  upDownImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(inH) :
        for k in range(inW) :
            outImage[inH-i-1][k] = inImage[i][k]

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

def mouseDrop(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, panYN
    if panYN == False :
        return
    ex = event.x;    ey = event.y
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    mx = sx - ex; my = sy - ey
    for i in range(inH) :
        for k in range(inW) :
            if  0 <= i-my < outW and 0 <= k-mx < outH :
                outImage[i-my][k-mx] = inImage[i][k]
    panYN = False
    displayImage()

# 영상 축소 알고리즘
def  zoomOutImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH//scale;  outW = inW//scale;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(outH) :
        for k in range(outW) :
            outImage[i][k] = inImage[i*scale][k*scale]

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
    for i in range(inH) :
        for k in range(inW) :
            outImage[i//scale][k//scale] += inImage[i][k]
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] //= (scale*scale)

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
    for i in range(outH) :
        for k in range(outW) :
            outImage[i][k] = inImage[i//scale][k//scale]

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
    for i in range(outH) :
        for k in range(outW) :
            rH = i / scale ; rW = k / scale
            iH = int(rH) ;  iW = int(rW)
            x = rW - iW; y = rH - iH
            if 0 <= iH < inH-1 and 0 <= iW < inW-1 :
                C1 = inImage[iH][iW]
                C2 = inImage[iH][iW+1]
                C3 = inImage[iH+1][iW+1]
                C4 = inImage[iH+1][iW]
                newValue = C1*(1-y)*(1-x) + C2*(1-y)* x+ C3*y*x + C4*y*(1-x)
                outImage[i][k] = int(newValue)

    displayImage()

# 영상 회전 알고리즘
def  rotateImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    for i in range(inH) :
        for k in range(inW) :
            xs = i ; ys = k;
            xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
            yd = int(math.sin(radian) * xs + math.cos(radian) * ys)
            if 0<= xd < inH and 0 <= yd < inW :
                outImage[xd][yd] = inImage[i][k]

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
    inCountList = [0] * 256
    outCountList = [0] * 256

    for i in range(inH) :
        for k in range(inW) :
            inCountList[inImage[i][k]] += 1

    for i in range(outH) :
        for k in range(outW) :
            outCountList[outImage[i][k]] += 1

    plt.plot(inCountList)
    plt.plot(outCountList)
    plt.show()

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
    inImage2 = []
    inImage2 = malloc(inH2, inW2)
    # 파일 --> 메모리
    with open(filename2, 'rb') as rFp:
        for i in range(inH2):
            for k in range(inW2):
                inImage2[i][k] = int(ord(rFp.read(1)))
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    #w1 = askinteger("원영상 가중치", "가중치(%)->", minvalue=0, maxvalue=100)
    #w2 = 1- (w1/100);    w1 = 1-w2

    import threading
    import time
    def morpFunc() :
        w1 = 1;        w2 = 0
        for _ in range(20) :
            for i in range(inH) :
                for k in range(inW) :
                    newValue = int(inImage[i][k]*w1 + inImage2[i][k]*w2)
                    if newValue > 255 :
                        newValue = 255
                    elif newValue < 0 :
                        newValue = 0
                    outImage[i][k] =newValue
            displayImage()
            w1 -= 0.05;        w2 += 0.05
            time.sleep(0.5)

    threading.Thread(target=morpFunc).start()


####################
#### 전역변수 선언부 ####
####################
inImage, outImage = [], [] ; inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
panYN = False
sx,sy,ex,ey = [0] * 4
####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝 기법) ver 0.03")

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
comVisionMenu2.add_command(label="명암대비", command=stretchImage)
comVisionMenu2.add_command(label="End-In탐색", command=endinImage)
comVisionMenu2.add_command(label="평활화", command=equalizeImage)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전", command=upDownImage)
comVisionMenu3.add_command(label="이동", command=moveImage)
comVisionMenu3.add_command(label="축소", command=zoomOutImage)
comVisionMenu3.add_command(label="확대", command=zoomInImage)
comVisionMenu3.add_command(label="회전1", command=rotateImage)
comVisionMenu3.add_command(label="회전2(중심,역방향)", command=rotateImage2)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="화소영역 처리", menu=comVisionMenu4)
comVisionMenu4.add_command(label="엠보싱", command=embossImage)

window.mainloop()