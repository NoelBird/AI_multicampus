import sys
import os
import markdown as md
import pdfkit
import imgkit


from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from formpy.ui_mainwindow2 import Ui_mainWindow
from formpy.ui_full_disp import Ui_Dialog

class Mainwin:
    def __init__(self):
        self.fname = ''
        view = QWebEngineView()
        view.setHtml("aaaaa")
        # super(Mainwin, self).__init__()
        btn = QPushButton()
        btn.move(200, 50)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # ui = Mainwin()
    # ui = Ui_Dialog()
    # ui.setupUi(MainWindow)
    # MainWindow.setWindowIcon(QIcon('logoico.ico'))
    # MainWindow.statusBar().showMessage('준비')
    # web = QWebEngineView()
    # web.setUrl(QUrl("https://www.google.com"))
    MainWindow.layout.addWidget() #TODO: 웹뷰 추가하기
    MainWindow.show()
    sys.exit(app.exec_())
