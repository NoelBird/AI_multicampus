from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import * # 입력받기. askinteger
from tkinter.filedialog import * # file dialog
import os

## 전역변수 선언부 ##
# dirName = "c:/images/Pet_GIF/Pet_GIF(256x256)/"
fnameList = []
photoList = [None]*6
num = 0 # 현재 사진 순번

## 함수 선언부 ##
def updateView():
    global num
    global fnameList
    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image=photo)  # 속성을 바꿔주는 기능
    lblFname.configure(text=fnameList[num])
    pLabel.photo = photo


def clickPrev():
    global num
    num -= 1
    if num < 0:
        num = len(fnameList) - 1
    updateView()


def clickLeft(event):
    txt = ''
    if event.num == 1:
        txt += '왼쪽 버튼:'
    elif event.num == 2:
        txt += '가운데 버튼'
    else:
        txt += '오른쪽 버튼:'
    txt += str(event.x) + ',' + str(event.y)
    messagebox.showinfo('요기제목', txt)


def clickNext():
    global num
    num += 1
    if num >= len(fnameList):
        num = 0
    updateView()


def clickHome():
    global num
    num = 0
    updateView()


def clickEnd():
    global num
    num = len(fnameList) - 1
    updateView()


def keyPress(event):
    global num
    curKey = event.keycode
    curKey = curKey - ord('0')
    if num + curKey >= len(fnameList):
        num = len(fnameList) - 1
    else:
        num += curKey
    updateView()


def jump(x):
    global num
    num = (num + x) % len(fnameList)
    updateView()


def fileClick():
    messagebox.showinfo('요기제목', '요기내용')


def hopImage(count=0):
    if count==0:
        count = askinteger("건너뛸 수", "숫자-->")
    for _ in range(count):
        clickNext()


def selectFile():
    global pLabel
    filename = askopenfilename(parent=window, filetypes=(("GIF파일", "*.gif"),("모든파일", "*.*")))
    pLabel.configure(text=str(filename))
    pLabel.text=filename

## 메인 코드부 ##
window = Tk()

window.title("GIF 사진 뷰어 (Ver 0.01")
window.geometry("600x400")
window.resizable(width=FALSE, height=TRUE)

folder = askdirectory(parent=window)
for dirName, subDirList, fnames in os.walk(folder):
    for fname in fnames:
        if os.path.splitext(fname)[1].lower() == '.gif':
            fnameList.append(os.path.join(dirName, fname))

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
menuMove = Menu(mainMenu)
menuJump = Menu(mainMenu)
# add cascade - 열리는거
# add command가 있음 - 뭔가 실행되는거
mainMenu.add_cascade(label='이동', menu=menuMove)
menuMove.add_command(label='앞으로', command=clickNext)
menuMove.add_command(label='뒤로', command=clickPrev)

mainMenu.add_cascade(label='건너뛰기', menu=menuJump)
menuJump.add_command(label='1', command=lambda:jump(1))
menuJump.add_command(label='3', command=lambda:jump(3))
menuJump.add_command(label='5', command=lambda:jump(5))
menuJump.add_command(label='원하는거', command=hopImage)
menuJump.add_command(label='파일열기', command=selectFile)


photo = PhotoImage(file= fnameList[num])
pLabel = Label(window, image=photo)


btnHome = Button(window, text='홈', command=clickHome)
btnPrev = Button(window, text='<< 이전 그림', command=clickPrev)
lblFname = Label(window, text=fnameList[num])
btnNext = Button(window, text='다음 그림>>', command=clickNext)
btnEnd = Button(window, text='마지막', command=clickEnd)

btnHome.place(x=50, y=10)
btnPrev.place(x=150, y=10)
lblFname.place(x=250, y=10)
btnNext.place(x=350, y=10)
btnEnd.place(x=450, y=10)
pLabel.place(x=15, y=50)
# label1 = Label(window, image=photo)

# label1.bind("<Button-1>", clickLeft)
window.bind("<Key>", keyPress)

# label1.pack(expand=1, anchor=CENTER)
window.mainloop()