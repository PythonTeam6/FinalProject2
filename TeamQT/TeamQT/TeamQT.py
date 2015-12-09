# coding: utf-8
 
import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
import re

from MP3 import *
from Video import *

if __name__ == '__main__':
    #melonParsing()

    #Video
    #app = QtWidgets.QApplication(sys.argv)
    #myWindow = VideoForm()
    #myWindow.show()
    #sys.exit(app.exec())
    
    #mp3
    app = QtWidgets.QApplication(sys.argv)
    myForm = Form()
    myForm.show()
    sys.exit(app.exec())