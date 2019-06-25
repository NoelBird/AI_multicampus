import sys
import os
import markdown as md
import pdfkit
import imgkit


from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from formpy.ui_mainwindow import Ui_mainWindow
from formpy.ui_full_disp import Ui_Dialog
# import Bokeh

class Mainwin(Ui_mainWindow):
    def __init__(self):
        self.fname = ''
        view = QWebEngineView()
        view.setHtml("aaaaa")
        # super(Mainwin, self).__init__()

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

    def saveIMG(self, fname):
        imgkit.from_string(md.markdown(self.txtMarkdown.toPlainText()), 'out.jpg')

    # def savePDF(self, fname):
    #     pdfkit.from_file(self.updatePreview(), 'out.pdf')

    def close(self):
        sys.exit()

    def updatePreview(self):
        try:
            curMD = md.markdown(self.txtMarkdown.toPlainText())
            # self.saveIMG('out.jpg')
        except Exception as e:
            pass
        finally:
            pixmap = QPixmap('out.jpg')
            self.lblPreview.setFixedSize(self.lblPreview.size())
            self.lblPreview.setPixmap(pixmap)








if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Mainwin()
    # ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.setWindowIcon(QIcon('logoico.ico'))
    web = QWebEngineView()
    web.setUrl(QUrl("https://www.google.com"))
    MainWindow.form_layout.addWidget(web)
    MainWindow.show()
    sys.exit(app.exec_())
