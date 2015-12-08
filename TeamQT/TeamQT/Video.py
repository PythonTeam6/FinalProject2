import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore

import shutil

class VideoForm(QtWidgets.QMainWindow):
    
    def resizeEvent(self ,resizeEvent):
        geo = self.frameGeometry()   
        self.setGeometry
        print(geo.width(), geo.height())
        
        width = geo.width()        
        height = geo.height()
        
        self.tableWidget.resize(int(width/2), int(height*481/600))
        
        self.tableWidget2.setGeometry(int(width/2), 50, int(width/2), int(height*481/600))
        self.tableWidget.setColumnWidth(0,int(width/2))
        self.tableWidget2.setColumnWidth(0,int(width/2))
        

        #QtWidgets.QMessageBox.information(self,"Information!","Window has been resized...")    
        #class TableSwitcher(QtWidgets.QTableWidget):
        #    def __init__(self, parent = Form):
        #        self = super().tableWidget
        #    def dropEvent(self, dropEvent):
        #        print("dropdropdrop")
        #        item_src = self.selectedItems()[0]
        #        print(item_src)
        #        item_dest = self.itemAt(dropEvent.pos())
        #        src_row = item_src.row()
        #        src_col = item_src.column()
        #        dest_value = item_dest.text()
        #        super(TableSwitcher,self).dropEvent(dropEvent)
        #        self.setItem(src_row,src_col, QtWidgets.QTableWidgetItem(dest_value))

  

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)        
        uic.loadUi("qt6.ui", self)
        
        geo = self.frameGeometry()        
        print(geo.width(), geo.height())
        width = geo.width()
        height = geo.height()
        
        self.row = 0
        self.row2 = 0
        self.videoFiles = []
        self.subFiles = []
        self.flag = False
        self.flag2 = False
        self.dragTemp = ''
        self.dragTemp2 = ''
        self.tempRow = 0
        self.tempRow2 = 0
        self.recentPath = ''
        
        self.tableWidget.setColumnWidth(0,int(width/2))
        self.tableWidget2.setColumnWidth(0,int(width/2))
        self.tableWidget.setRowCount(self.row)
        self.tableWidget2.setRowCount(self.row2)
        
        self.tableWidget.cellEntered.connect(self.OnDragIn)        #�巡�� ��
        self.tableWidget.cellChanged.connect(self.OnDragOut)              #�巡�� �ƿ�
        self.tableWidget.cellDoubleClicked.connect(self.OnDelete)

        self.tableWidget2.cellEntered.connect(self.OnDragIn2)        #�巡�� ��
        self.tableWidget2.cellChanged.connect(self.OnDragOut2)              #�巡�� �ƿ�
        self.tableWidget2.cellDoubleClicked.connect(self.OnDelete2)
        #self.tableWidget.itemSelectionChanged.connect(self.OnDragOut)
               
        self.actionAdd_Videos.setShortcut('Ctrl+V')
        self.actionAdd_Videos.setStatusTip('Open new Video Files')
        self.actionAdd_Videos.triggered.connect(self.OnClickAddVideos)
        
        self.actionAdd_Subtitues.setShortcut('Ctrl+S')
        self.actionAdd_Subtitues.setStatusTip('Open new Sub Files')
        self.actionAdd_Subtitues.triggered.connect(self.OnClickAddSubs)

        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.setStatusTip('Terminate Program')
        self.actionExit.triggered.connect(self.OnClickExit)
        
        self.button.pressed.connect(self.OnClickAddVideos)
        self.button2.pressed.connect(self.OnClickAddSubs)
        self.button3.pressed.connect(self.OnClickMatch)
                

    def OnDelete(self, row, col):
        print(row, col)
        print("double Clicked")
        del self.videoFiles[row]
        self.row = len(self.videoFiles)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(self.row)
        for k in range(self.row):
            newitem = QtWidgets.QTableWidgetItem()                
            newitem.setText(self.videoFiles[k])
            self.tableWidget.setItem(k, 0, newitem)                
            
    def OnDragOut(self, row, col):               
        if self.flag2 and not(self.flag):
            self.tableWidget.cellChanged.disconnect()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(self.row)
            for k in range(self.row):
                newitem = QtWidgets.QTableWidgetItem()                
                newitem.setText(self.videoFiles[k])
                self.tableWidget.setItem(k, 0, newitem)      
            self.tableWidget.cellChanged.connect(self.OnDragOut)  
        if self.flag:
            print(self.row, row)
            print("row count {0:d}".format(self.tableWidget.rowCount()))
            if self.tableWidget.rowCount() > self.row:
                self.tableWidget.cellChanged.disconnect()
                self.tableWidget.setRowCount(0)
                self.tableWidget.setRowCount(self.row)
                for k in range(self.row):
                    newitem = QtWidgets.QTableWidgetItem()                
                    newitem.setText(self.videoFiles[k])
                    self.tableWidget.setItem(k, 0, newitem)      
                self.tableWidget.cellChanged.connect(self.OnDragOut)   
            elif self.row == row:
                self.tableWidget.setRowCount(self.row)
            else :
                print(self.videoFiles[row])
                self.dragTemp = self.videoFiles[row]
                self.videoFiles[row] = self.videoFiles[self.tempRow]
                self.videoFiles[self.tempRow] = self.dragTemp

                self.tableWidget.cellChanged.disconnect()
                newitem = QtWidgets.QTableWidgetItem()                
                newitem.setText(self.videoFiles[row])
                self.tableWidget.setItem(row, 0, newitem)  

                newitem = QtWidgets.QTableWidgetItem()                
                newitem.setText(self.videoFiles[self.tempRow])
                self.tableWidget.setItem(self.tempRow, 0, newitem)  
                self.tableWidget.cellChanged.connect(self.OnDragOut)
            print("DragOut")
            self.flag = False
            

    def OnDragIn(self):
        self.tempRow = self.tableWidget.currentRow()
        self.flag = True
        print("DragIn")

    def OnDelete2(self, row, col):
        
        print(row, col)
        print("double Clicked")
        del self.subFiles[row]
        self.row2 = len(self.subFiles)
        self.tableWidget2.setRowCount(0)
        self.tableWidget2.setRowCount(self.row2)
        for k in range(self.row2):
            newitem = QtWidgets.QTableWidgetItem()                
            newitem.setText(self.subFiles[k])
            self.tableWidget2.setItem(k, 0, newitem)                
            
    def OnDragOut2(self, row, col):               
        if self.flag and not(self.flag2):
            self.tableWidget2.cellChanged.disconnect()
            self.tableWidget2.setRowCount(0)
            self.tableWidget2.setRowCount(self.row2)
            for k in range(self.row2):
                newitem = QtWidgets.QTableWidgetItem()                
                newitem.setText(self.subFiles[k])
                self.tableWidget2.setItem(k, 0, newitem)      
            self.tableWidget2.cellChanged.connect(self.OnDragOut2)  
        if self.flag2:
            print(self.row2, row)
            print("row count {0:d}".format(self.tableWidget2.rowCount()))
            if self.tableWidget2.rowCount() > self.row2:
                self.tableWidget2.cellChanged.disconnect()
                self.tableWidget2.setRowCount(0)
                self.tableWidget2.setRowCount(self.row2)
                for k in range(self.row2):
                    newitem = QtWidgets.QTableWidgetItem()                
                    newitem.setText(self.subFiles[k])
                    self.tableWidget2.setItem(k, 0, newitem)      
                self.tableWidget2.cellChanged.connect(self.OnDragOut2)   
            elif self.row2 == row:
                self.tableWidget2.setRowCount(self.row2)
            else :
                print(self.subFiles[row])
                self.dragTemp2 = self.subFiles[row]
                self.subFiles[row] = self.subFiles[self.tempRow2]
                self.subFiles[self.tempRow2] = self.dragTemp2

                self.tableWidget2.cellChanged.disconnect()
                newitem = QtWidgets.QTableWidgetItem()                
                newitem.setText(self.subFiles[row])
                self.tableWidget2.setItem(row, 0, newitem)  

                newitem = QtWidgets.QTableWidgetItem()                
                newitem.setText(self.subFiles[self.tempRow2])
                self.tableWidget2.setItem(self.tempRow2, 0, newitem)  
                self.tableWidget2.cellChanged.connect(self.OnDragOut2)
            print("DragOut")
            self.flag2 = False
            

    def OnDragIn2(self):
        self.tempRow2 = self.tableWidget2.currentRow()
        self.flag2 = True
        print("DragIn")


    def OnClickExit(self):
        QtWidgets.QApplication.quit()

    def OnClickMatch(self):
        print("match button pushed")
        if len(self.videoFiles) != 0 and len(self.subFiles) != 0:
            if len(self.videoFiles) == len(self.subFiles):
                for i in range(len(self.videoFiles)):
                    t, videoName = os.path.split(self.videoFiles[i])    #video 이름 받기
                    videoName, t = os.path.splitext(videoName)
                    videoPath, t = os.path.splitext(self.videoFiles[i]) #video Path 받기

                    t, subName = os.path.split(self.subFiles[i])    # 자막 이름 받기
                    t, etc = os.path.splitext(self.subFiles[i])     # 자막 확장자 받기
                    
                    print(subName, '\n->', videoName + etc)
                    os.rename(self.subFiles[i], videoPath + etc)  # 파일 이름바꾸기
                    #shutil.copy(self.subFiles[i], videoPath + etc)    # 파일 복사
            else:
                print('video와 sub의 갯수가 다름')
        else:
            print('video나 sub가 비었음')

    def OnClickAddVideos(self):
        (a, b) = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', self.recentPath, 'Video Files (*.avi *.mp4 *.wmv *.mpeg *.mpg *.flv *.asf *.mov *.mkv);;All Files (*.*)')
        if len(self.videoFiles) == 0:
            self.videoFiles = a
        else:
            for l in a:
                if l not in self.videoFiles:
                    self.videoFiles.append(l)
                    self.recentPath, etc = os.path.split(l)

        if len(self.videoFiles) == 0:
            return
        else:            
            for k in range(len(self.videoFiles) - self.row):
                self.tableWidget.setRowCount(len(self.videoFiles))
                newitem = QtWidgets.QTableWidgetItem()                
                newitem.setText(self.videoFiles[k+self.row])
                self.tableWidget.setItem(k+self.row, 0, newitem)                
            self.row = len(self.videoFiles)
    
    def OnClickAddSubs(self):
        (a, b) = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', self.recentPath, 'Sub Files (*.smi);;All Files (*.*)')
        if len(self.subFiles) == 0:
            self.subFiles = a
        else:
            for l in a:
                if l not in self.subFiles:
                    self.subFiles.append(l)
                    self.recentPath, etc = os.path.split(l)

        if len(self.subFiles) == 0:
            return
        else:            
            for k in range(len(self.subFiles) - self.row2):
                self.tableWidget2.setRowCount(len(self.subFiles))
                newitem = QtWidgets.QTableWidgetItem()                
                newitem.setText(self.subFiles[k+self.row2])
                self.tableWidget2.setItem(k+self.row2, 0, newitem)                
            self.row2 = len(self.subFiles)