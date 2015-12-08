import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from mutagen.easyid3 import EasyID3

from Web_Parser import *

class Form(QtWidgets.QMainWindow):
    
    def resizeEvent(self ,resizeEvent):
        geo = self.frameGeometry()   
        #print(geo.width(), geo.height())
        
        width = geo.width()
        height = geo.height()

        self.tableWidget.resize(width, int(height*475/631))
        self.tableWidget.setColumnWidth(0,int(width*1/self.divide))
        self.tableWidget.setColumnWidth(1,int(width*3/self.divide))
        self.tableWidget.setColumnWidth(2,int(width*2/self.divide))
        self.tableWidget.setColumnWidth(3,int(width*2.3/self.divide))
        #QtWidgets.QMessageBox.information(self,"Information!","Window has been resized...")    
    

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        
        #self.ui = uic.loadUi("qt3.ui")        
        uic.loadUi("qtMp3.ui", self)
        
        geo = self.frameGeometry()        
        print(geo.width(), geo.height())
        
        width = geo.width()
        height = geo.height()
        
        self.files = []
        self.row = 0
        self.tempRow = 0
        self.dragTemp = ''
        self.flag = False
        self.divide = 9
        
        self.tableWidget.resize(width, int(height*475/631))
        self.tableWidget.setColumnWidth(0,int(width*1/self.divide))
        self.tableWidget.setColumnWidth(1,int(width*3/self.divide))
        self.tableWidget.setColumnWidth(2,int(width*2/self.divide))
        self.tableWidget.setColumnWidth(3,int(width*2.3/self.divide))
        
        self.tableWidget.setRowCount(self.row)
              
        self.tableWidget.cellDoubleClicked.connect(self.OnDelete)

        self.actionAdd_Files.setShortcut('Ctrl+O')
        self.actionAdd_Files.setStatusTip('Open new File')
        self.actionAdd_Files.triggered.connect(self.OnClickAdd)
        
        self.convertButton.pressed.connect(self.OnClickConvert)
        self.addButton.pressed.connect(self.OnClickAdd)
        self.formatButton.pressed.connect(self.OnClickFormat)
        self.pathButton.pressed.connect(self.OnClickPath)
        #self.show()

    def OnDelete(self, row, col):
        print(row, col)
        print("double Clicked")
        del self.files[row]
        self.row = len(self.files)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(self.row)
        for k in range(self.row):
            newitem = QtWidgets.QTableWidgetItem()                
            newitem.setText("unChanged")
            self.tableWidget.setItem(k, 0, newitem)       
            newitem = QtWidgets.QTableWidgetItem()                
            newitem.setText(self.files[k])
            self.tableWidget.setItem(k, 1, newitem)   
            newitem = QtWidgets.QTableWidgetItem()                
            newitem.setText(os.path.basename(self.files[k]))
            self.tableWidget.setItem(k, 2, newitem)            
            
    def nameParse(self, file):
        audio = EasyID3(file)
        t, fileName = os.path.split(file)
        fileName, t = os.path.splitext(fileName)
        print(fileName)

        keys = audio.valid_keys.keys()

        p = re.compile('\w+')
        names = p.findall(fileName)

        print(names)
        return names

    def OnClickConvert(self):
        if len(self.files) == 0:
            print('파일이 없당.')
            return

        path = []
        file = []
        for item in self.files:
            p, f = os.path.split(item)
            path.append(p)
            file.append(f)

        #'Ariana+-+Grande+-+Problem.mp3'
        #'Daft+-+Punk+-+ Harder+-+Better+-+Faster+-+Stronger.mp3'
        jparse = JSON_Parser()
        for i in range(len(path)):
            print(file[i])
            parseList = self.nameParse(file[i])
            song, artist = jparse.matchSongname(parseList)
            os.rename(path[i]+'/'+file[i], path[i]+'/'+artist+'-'+song+'.mp3')


        
    def OnClickFormat(self):
        print("I'm format Button")

    def OnClickPath(self):
        print("I'm path Button")
    
    def OnClickAdd(self):
        (a, b) = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', '', 'Music Files (*.mp3 *.wav *.flac);;All Files (*.*)')
        if len(self.files) == 0:
            self.files = a
        else:
            for l in a:
                if l not in self.files:
                    self.files.append(l)
        if len(self.files) == 0:
            return
        else:       
            for k in range(len(self.files) - self.row):
                self.tableWidget.setRowCount(len(self.files))
                newitem = QtWidgets.QTableWidgetItem()                
                newitem.setText("unChanged")
                self.tableWidget.setItem(k+self.row, 0, newitem)            
                newitem = QtWidgets.QTableWidgetItem()                
                newitem.setText(self.files[k+self.row])
                self.tableWidget.setItem(k+self.row, 1, newitem)      
                newitem = QtWidgets.QTableWidgetItem()                
                newitem.setText(os.path.basename(self.files[k+self.row]))
                self.tableWidget.setItem(k+self.row, 2, newitem)  
            self.row = len(self.files)

    def test(self):
        audio = EasyID3("Harder, Better, Faster, Stronger.mp3")
        audio2 = EasyID3("Jessie+J-01-Bang+Bang.mp3")
        keys = audio.valid_keys.keys()
        keys2 = audio2.valid_keys.keys()
        for key in keys:
            try:
                print(key, ' : ', audio[key])
            except:
                pass
        for key in keys2:
            try:
                print(key, ' : ', audio2[key])
            except:
                pass
        #audio.save()