# coding: utf-8
 
import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

from mutagen.easyid3 import EasyID3
import re

from Web_Parser import *
from MP3 import *
from Video import *
    


def nameParse(file):
    audio = EasyID3(file)
    t, fileName = os.path.split(file)
    fileName, t = os.path.splitext(fileName)
    print(fileName)

    keys = audio.valid_keys.keys()

    p = re.compile('\w+')
    names = p.findall(fileName)

    print(names)
    return names


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

    l = nameParse('노라조 - 치이고 박히고 무능상사.mp3')
    jparse = JSON_Parser()
    print(jparse.matchSongname(l))