from tkinter import *
from tkinter.simpledialog import *

from tkinter.filedialog import *
import math
import os
import os.path


#####################
#### 함수 선언부 ####
#####################
def malloc(h, w):
    retMemory = []
    for _ in range(h):
        tmpList = []
        for _ in range(w):
            tmpList.append(0)
        retMemory.append(tmpList)
    return retMemory



# 파일을 메모리로 로딩하는 함수
def loadImage(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = os.path.getsize(fname) # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize)) # 핵심 코드, 폭과 높이 가져옴(정사각형 이미지)

    ## 입력영상 메모리 확보 ##
    inImage = []
    inImage = malloc(inH, inW)

    # 파일 --> 메모리
    with open(filename, 'rb') as rFp:
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rFp.read(1))) # 1바이트만 읽음


# 파일을 선택해서 메모리로 로딩하는 함수
def openImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW파일", "*.raw"), ("모든파일", "*.*")))
    loadImage(filename)
    equalImage()



def saveImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    pass


def displayImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None: # 예전에 실행한 적이 있다.
        canvas.destroy()
    ## 화면 크기를 조절
    window.geometry(str(outH) + 'x' + str(outW)) # 벽
    canvas = Canvas(window, height=outH, width=outW) # 보드
    paper = PhotoImage(height=outH, width=outW) # 빈 종이
    canvas.create_image((outH//2, outW//2), image=paper, state='normal')
    ## 출력영상 --> 화면에 한점씩 찍자.
    for i in range(outH):
        for k in range(outW):
            r = g = b = outImage[i][k]
            paper.put("#%02x%02x%02x" % (r, g, b), (k, i))
    canvas.pack(expand=1, anchor=CENTER)

####################################################
##### 컴퓨터 비전(영상처리) 알고리즘 함수 모음 #####
####################################################

# 동일영상 알고리즘
def equalImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    ##### 메모리 할당 #############
    outImage = []
    outImage = malloc(outH, outW)
    ##### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]

    displayImage()


def rot90Image():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    ##### 메모리 할당 #############
    outImage = []
    outImage = malloc(outH, outW)
    ##### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(inH):
        for k in range(inW):
            outImage[inH-k-1][inW-i-1] = inImage[i][k]
    displayImage()

def moveImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    ##### 메모리 할당 #############
    outImage = []
    outImage = malloc(outH, outW)
    ##### 진짜 컴퓨터 비전 알고리즘 #####
    deltaX = askinteger('이동', '이동할 x값 -->', minvalue=-255, maxvalue=255)
    deltaY = askinteger('이동', '이동할 y값 -->', minvalue=-255, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            newY = deltaY + i
            newX = deltaY + k
            if newX >= 0 and newX <= 255 and newY >= 0 and newY <= 255:
                outImage[newY][newX] = inImage[i][k]
    displayImage()


def squeezeImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW

    mag = askinteger('축소', '축소할 배율(2 또는 4) -->', minvalue=2, maxvalue=4)
    outH //= mag
    outW //= mag
    ##### 메모리 할당 #############
    outImage = []
    outImage = malloc(outH, outW)
    ##### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i*mag][k*mag]
    displayImage()


def expandImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW

    mag = askinteger('확대', '확대할 배율(2의 배수) -->', minvalue=2)
    outH *= mag
    outW *= mag
    ##### 메모리 할당 #############
    outImage = []
    outImage = malloc(outH, outW)
    ##### 진짜 컴퓨터 비전 알고리즘 #####

    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i//mag][k//mag]
    displayImage()


# def rotFreeImage():
#     global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
#     outH = inH
#     outW = inW
#
#     ##### 메모리 할당 #############
#     outImage = []
#     outImage = malloc(outH, outW)
#     ##### 진짜 컴퓨터 비전 알고리즘 #####
#     ang = askinteger('회전', '회전할 각도 -->', minvalue=0, maxvalue=360) / 180*math.pi
#     centerX = outW // 2
#     centerY = outH // 2
#
#     for i in range(outH):
#         for k in range(outW):
#             R = ((k - centerX)**2 + (i - centerY)**2)**0.5
#             if(k-centerX == 0):
#                 continue
#             curAng = math.acos((k - centerX)/R)
#             newAng = curAng - ang
#             newX = centerX + int(R*math.cos(newAng))
#             newY = centerY - int(R*math.sin(newAng))
#
#             if newX >= 0 and newX <= 255 and newY >= 0 and newY <= 255:
#                 outImage[newY][newX] = inImage[i][k]
#     displayImage()



#########################
#### 전역변수 선언부 ####
#########################
inImage, outImage = [], []
inH, inW, outH, outW = [0]*4 # inW, inH는 들어오는 파일 캔버스의 가로세로
window, canvas, paper = None, None, None
filename = "" # db에 넣어도 키 처럼 사용하려고 하는거에요

#####################
#### 메인 코드부 ####
#####################
# 메인 코드  부분
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝 기법) Ver 0.01")

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImage)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImage)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="오른쪽90도회전", command=rot90Image)
comVisionMenu1.add_command(label="상하좌우 이동", command=moveImage)
comVisionMenu1.add_command(label="축소", command=squeezeImage)
comVisionMenu1.add_command(label="확대", command=expandImage)
# comVisionMenu1.add_command(label="회전(각도입력)", command=rotFreeImage)


window.mainloop()