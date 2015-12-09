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
        
        self.setWindowTitle('더 어블클릭')
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
        self.myPath = '.'
        self.myFormat = '-'
        
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

    def getFileInfo(self, file):
        audio = EasyID3(file)
        artist = None
        title = None
        try:
            title = audio['title'][0]
            artist = audio['artist'][0]
        except KeyError:
            pass
        print(title, artist)
        return title, artist

    def nameParse(self, file):
        t, fileName = os.path.split(file)
        fileName, t = os.path.splitext(fileName)
        print(fileName)

        p = re.compile('\w+')
        names = p.findall(fileName)

        print(names)
        return names

    def OnClickConvert(self):
        if len(self.files) == 0:
            QtWidgets.QMessageBox.information(self,"주의!","파일을 먼저 추가하십시오.")
            return

        path = []
        file = []
        file_info = []
        for item in self.files:
            title, artist = self.getFileInfo(item)
            p, f = os.path.split(item)
            path.append(p)
            file.append(f)
            if title == None or artist == None:
                file_info.append(f)
            else:
                file_info.append(artist+' '+title)
        ###################################################################

        #'Ariana+-+Grande+-+Problem.mp3'
        #'Daft+-+Punk+-+ Harder+-+Better+-+Faster+-+Stronger.mp3'
        jparse = JSON_Parser()
        for i in range(len(path)):
            print(file_info[i])
            parseList = self.nameParse(file_info[i])
            song, artist = jparse.matchSongname(parseList)
            os.rename(path[i]+'/'+file[i], self.myPath+'/'+artist+self.myFormat+song+'.mp3')
                    
            newitem = QtWidgets.QTableWidgetItem()                
            newitem.setText("Changed")
            self.tableWidget.setItem(i, 0, newitem)       
            newitem = QtWidgets.QTableWidgetItem()                
            newitem.setText(artist+self.myFormat+song+'.mp3')
            self.tableWidget.setItem(i, 3, newitem)      
        
    def OnClickFormat(self):
        print("I'm format Button")
        text, result = QtWidgets.QInputDialog.getText(self, "Set Format", "Artist + \"  \" + Song 안에 들어갈 기호를 설정하세요.")
        if result:
            self.myFormat = text
            print(self.myFormat)

    def OnClickPath(self):
        print("I'm format Button")
        text, result = QtWidgets.QInputDialog.getText(self, "Set Format", "path를 입력하세요")
        if result:
            self.myPath = text
            print(self.myPath)
    
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