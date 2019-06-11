from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import * # for askinteger


## 함수 선언 부분 ##
def func_open():
    global photo
    filename = askopenfilename(parent = window, filetypes = (("GIF 파일", "*.gif"),
                                                             ("모든 파일", "*.*")))
    photo = PhotoImage(file = filename)
    pLabel.configure(image = photo)
    pLabel.image = photo


def func_exit():
    window.quit()
    window.destroy()


def func_zoom_in():
    global photo, pLabel
    mag = int(askinteger("확대배수", "확대할 배수를 입력하세요(2~8)"))
    photo = photo.zoom(mag, mag)
    pLabel.configure(image=photo)
    pLabel.image = photo



def func_zoom_out():
    global photo, pLabel
    mag = int(askinteger("축소배수", "축소할 배수를 입력하세요(2~8)"))
    photo = photo.subsample(mag, mag)
    pLabel.configure(image=photo)
    pLabel.image = photo


## 메인 코드 부분 ##
window = Tk()
window.geometry("400x400")
window.title("명화 감상하기")

photo = PhotoImage()
pLabel = Label(window, image = photo)
pLabel.pack(expand = 1, anchor = CENTER)

mainMenu = Menu(window)
window.config(menu = mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label = '파일', menu=fileMenu)
fileMenu.add_command(label = '파일 열기', command = func_open)
fileMenu.add_separator()
fileMenu.add_command(label = '프로그램 종료', command = func_exit)

expandMenu = Menu(mainMenu)
mainMenu.add_cascade(label = '이미지 효과', menu=expandMenu)
expandMenu.add_command(label = '확대하기', command = func_zoom_in)
expandMenu.add_command(label = '축소하기', command = func_zoom_out)

window.mainloop()