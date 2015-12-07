# coding: utf-8
 
import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

from DB_Control import *
from Web_Parser import *
from MP3 import *
from Video import *


def melonParsing():
    dbc = DBControl("test.db")
    artistDB = DBControl("artist.db")

    l = list(artistDB.getDataList())
    print(l)

    jparse = JSON_Parser()
    l = list(dbc.getDataList())
    
    #str = ('You Kyung',)
    #l = l[l.index(str):]

    #dbc.init_DB()
    #for item in l:
    #    result = artistDB.findArtist(item[0]).fetchall()
    #    if len(result) == 0:
    #        artists = jparse.request_Melon(item[0])
    #        for artist in artists:
    #            result = artistDB.findArtist(artist).fetchall()
    #            if len(result) == 0:
    #                print(artist)
    #                artistDB.insertData(artist)
    #    else:
    #        print('Overlap\n')

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