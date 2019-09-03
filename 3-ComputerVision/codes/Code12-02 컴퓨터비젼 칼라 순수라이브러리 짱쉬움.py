from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

# 파일을 선택해서 메모리로 로딩하는 함수
import time
def openImagePIL() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return

    inImage = Image.open(filename)
    inW = inImage.width
    inH = inImage.height

    outImage = inImage.copy()
    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def displayImagePIL() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    VIEW_X = outW;    VIEW_Y = outH;   step = 1
    window.geometry(str(int(VIEW_Y*1.2)) + 'x' + str(int(VIEW_X*1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    rgbImage = outImage.convert('RGB')
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0,outH, step) :
        tmpStr = ''
        for k in numpy.arange(0,outW, step) :
            i = int(i); k = int(k)
            r , g, b = rgbImage.getpixel((k,i))
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

def saveImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if outImage == None :
        return
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='*.jpg', filetypes=(("JPG 파일", "*.jpg"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    outImage.save(saveFp.name)
    print('Save~')

def addImagePIL() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    value = askfloat("밝게/어둡게", "값(0~16)-->", minvalue=0.0, maxvalue=16.0)
    outImage = inImage.copy()
    outImage = ImageEnhance.Brightness(outImage).enhance(value)
    outW = outImage.width
    outH = outImage.height
    displayImagePIL()

def blurImagePIL() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outImage = inImage.copy()
    outImage = outImage.filter(ImageFilter.BLUR)
    outW = outImage.width
    outH = outImage.height
    displayImagePIL()

def zoominImagePIL() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값(2~8)-->", minvalue=2, maxvalue=8)
    outImage = inImage.copy()
    outImage = outImage.resize((inH*scale, inW*scale))
    outW = outImage.width
    outH = outImage.height
    displayImagePIL()
####################
#### 전역변수 선언부 ####
####################
inImage, outImage = None, None ;
inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)
####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(칼라 라이브러리) ver 0.01")

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

## 마우스 이벤트


mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImagePIL)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImagePIL)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="덧셈/뺄셈", command=addImagePIL)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="화소영역 처리", menu=comVisionMenu2)
comVisionMenu2.add_command(label="블러링", command=blurImagePIL)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학적 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="확대", command=zoominImagePIL)


window.mainloop()