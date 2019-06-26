import sys
import os
import markdown as md

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap, QClipboard
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QHBoxLayout, QDialog
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QDir
from formpy.ui_mainwindow2 import Ui_mainWindow
import PyQt5.QtCore as QtCore
from formpy.ui_full_disp import Ui_Dialog


class Mainwin(Ui_mainWindow):
    def __init__(self):
        super(Mainwin, self).__init__()
        self.fname = ''
        self.template = ''


    def openFile(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # TODO: 상속하는 부분 개선하기 None -> ?
        fileName, _ = QFileDialog.getOpenFileName(None, "열기", "","Markdown(*.md);;Power Point(*.pptx | *.ppt);;All Files (*)", options=options)

        if fileName:
            # TODO: file에서 dot(.)이 여러개일 경우에 에러가 없는지 체크
            ext = os.path.splitext(fileName)[1]
            if ext == '.md':
                self.loadMD(fileName)
            # if ext.lower() in ['.ppt', '.pptx']:

    # TODO: 특정한 디렉토리 내에서는 오픈이 안되는 이슈가 있습니다.
    def loadMD(self, fname):
        print(fname)
        with open(fname, "r") as fp:
            txt = fp.read()
            self.txtMarkdown.setText(txt)

    def saveFile(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # TODO: 상속하는 부분 개선하기 None -> ?
        fileName, _ = QFileDialog.getSaveFileName(None, "저장", "",
                                                  "Markdown(*.md);;Power Point(*.pptx | *.ppt);;All Files (*)",
                                                  options=options)

        if fileName:
            # TODO: file에서 dot(.)이 여러개일 경우에 에러가 없는지 체크
            ext = os.path.splitext(fileName)[1]
            if ext == '.md':
                self.saveMD(fileName)
            # if ext.lower() in ['.ppt', '.pptx']:

    def saveMD(self, fname):
        with open(fname, "wt") as fp:
            fp.write(self.txtMarkdown.toPlainText())

    # def savePDF(self, fname):
    #     pdfkit.from_file(self.updatePreview(), 'out.pdf')

    def close(self):
        sys.exit()

    def mdfullScreen(self):
        self.showFullScreen()

    def updateWeb(self):
        try:
            curMD = md.markdown(self.txtMarkdown.toPlainText())
            baseDir = "C:\\Users\\user\\Documents\\Python-programming\\quick-point"
            css = "<link rel=\"stylesheet\" type=\"text/css\" href=\"templates/template1.css\"><br>"
            totalHtml = "<div class='markdown-body'>" + css + '\n' + curMD +"</div>"
            with open("curHtml.html", "wt") as fp:
                fp.write(totalHtml)
            print(css+curMD)
            # self.wgtWeb.setHtml(css+curMD)
            print(QDir.currentPath() + '/curHtml.html')
            self.wgtWeb.setUrl(QUrl.fromLocalFile(QDir.currentPath() + '/curHtml.html'))

        except Exception as e:
            pass
        finally:
            pass
            # pixmap = QPixmap('out.jpg')
            # self.lblPreview.setFixedSize(self.lblPreview.size())
            # self.lblPreview.setPixmap(pixmap)

#
# class ctrlWin(QtWidgets.QMainWindow):
#     cnt = 0
#     def __init__(self):
#         self.win = QtWidgets.QMainWindow()
#         ui = Mainwin()
#         ui.setupUi(self.win)
#         self.win.setWindowIcon(QIcon('logoico.ico'))
#         self.win.statusBar().showMessage('준비')
#         self.wgtWeb = self.win.findChild(QWebEngineView)
#
#         self.win.txtMarkdown.connect()
#         self.win.show()
#
#     def updateWindow(self):
#         self.wgtWeb.setHtml("%d" % ctrlWin.cnt)
#         ctrlWin += 1
#         # submitFrame = self.subwindow.findChild(QtGui.QFrame, "frameSubmit")

def showFullScreen(mainwin):
    pass
    wgt = QDialog()
    wgt.showFullScreen()
    # wgt.setWindowFlags(QtCore.Qt.Window | )
    wgt.showFullScreen()
    wgt.
    wgt.exec_()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # wmain = ctrlWin()
    MainWindow = QtWidgets.QMainWindow()
    ui = Mainwin()
    ui.setupUi(MainWindow)
    MainWindow.setWindowIcon(QIcon('logoico.ico'))
    MainWindow.statusBar().showMessage('준비')
    # web = QWebEngineView()
    # web.setUrl(QUrl("https://www.google.com"))
    # web.setHtml("aaaaa")
    # MainWindow.findChild(QHBoxLayout).addWidget(web) #TODO: 웹뷰 추가하기
    # MainWindow.findChild(QWebEngineView).setHtml('aaaa')
    # web.move()
    MainWindow.show()  # 창 화면으로 화면 띄우기
    # MainWindow.showFullScreen()  # 전체화면으로 화면을 띄우기
    showFullScreen(MainWindow)
    sys.exit(app.exec_())
