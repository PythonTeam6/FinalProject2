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

def nameParse2(file):
    audio = EasyID3(file)
    t, fileName = os.path.split(file)
    fileName, t = os.path.splitext(fileName)
    print(fileName)

    keys = audio.valid_keys.keys()

    p = re.compile('\w+')
    names = p.findall(fileName)


    length = len(names)
    name = ''

    for i in range (length):
        for num in range(length-i):
            if name == '':
                name = names[num+i]
            else:
                name = name + ' ' + names[num+i]
            #print('{0:d} + {1:d} = {2:d}'.format(i,num,names))
            #print(name)
            if name == audio['artist'][0]: #'Faster Stronger'
                for k in range(num+1):
                    #print(num, ' ', names[i])
                    names.pop(i)
                #print('result : ', names[i:i+num+1])
                print(names, name)
                return names, name  # 나머지부분, 파싱되는 값
        name = ''

    return names, None


if __name__ == '__main__':
    #melonParsing()

    #Video
    #app = QtWidgets.QApplication(sys.argv)
    #myWindow = VideoForm()
    #myWindow.show()
    #sys.exit(app.exec())
    
    #mp3
    #app = QtWidgets.QApplication(sys.argv)
    #myForm = Form()
    #myForm.show()
    #sys.exit(app.exec())

    #l, artist = nameParse('노라조 - 치이고 박히고 무능상사.mp3')
    l = nameParse('노라조 - 치이고 박히고 무능상사.mp3')
    jparse = JSON_Parser()
    #jparse.matchSongname(l, artist)
    jparse.matchSongname(l)