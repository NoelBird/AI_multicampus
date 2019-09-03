import os
baseDir = "C:/Users/user/Documents/Python-programming/quick-point/"
srcDir = "ui"
dstDir = "formpy"
inFile = "mainwindow2.ui"  # mainwindow.ui
outFile = "ui_" + '.'.join(inFile.split('.')[:-1]) + '.py'
os.system("python -m PyQt5.uic.pyuic -x %s -o %s" % (os.path.join(baseDir, srcDir, inFile),
                                                     os.path.join(baseDir, dstDir, outFile)))
