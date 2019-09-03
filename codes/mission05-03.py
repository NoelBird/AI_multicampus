from tkinter import *

from tkinter import messagebox
from tkinter.simpledialog import * # 입력받기. askinteger
from tkinter.filedialog import * # file dialog
import os

## 전역변수 선언부 ##

## 함수 선언부 ##


def readTxt(fname):
    global txtMain
    with open(fname) as inFp:
        content = inFp.readlines()
        txtMain.delete(1.0, tkinter.END)
        txtMain.insert(1.0, '\n'.join(content))


def saveTxt(fname):
    global txtMain
    with open(fname.name, "w") as outFp:
        outFp.write(str(txtMain.get(1.0, tkinter.END)))
    messagebox.showinfo('저장', '파일이 저장되었습니다.')

def clickOpen():
    fname = askopenfilename(parent=window, filetypes=(("TXT파일", "*.txt"), ("모든파일", "*.*")))
    readTxt(fname)

def clickSave():
    fname = asksaveasfile(parent=window, filetypes=(("TXT파일", "*.txt"), ("모든파일", "*.*")), defaultextension='.txt',
                          mode='w')
    saveTxt(fname)

def clickReplace():
    pass

## 메인 코드부 ##
window = Tk()

window.title("NOTPAD (Ver 0.01)")
window.geometry("600x400")
window.resizable(width=FALSE, height=TRUE)


mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
editMenu = Menu(mainMenu)
# add cascade - 열리는거
# add command가 있음 - 뭔가 실행되는거
mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=clickOpen)
fileMenu.add_command(label='저장', command=clickSave)

mainMenu.add_cascade(label='편집', menu=editMenu)
editMenu.add_command(label='바꾸기', command=clickReplace)


txtMain = Text()


txtMain.pack(expand=1, anchor=CENTER)

# window.bind("<Key>", keyPress)

# label1.pack(expand=1, anchor=CENTER)
window.mainloop()