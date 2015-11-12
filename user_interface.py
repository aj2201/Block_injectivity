# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 17:18:52 2015

@author: Aygul.Ibatullina
"""
from PyQt4 import QtCore, QtGui
import sys
from BlockInjIndex import BlockInjIndex
from Ui_AboutWidget import Ui_AboutWidget
from Ui_MainWindow import Ui_MainWindow

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
        
        
        

  
class user_interface(Ui_MainWindow):
    
    def setupUi2(self, MainWindow):
        self.setupUi(MainWindow)
        self.setup_file_open_dialogs()
        #QtCore.QObject.connect(self.start_time_edit, QtCore.SIGNAL(_fromUtf8("dateChanged(QDate)")), self.menubar.raise_)
        QtCore.QObject.connect(self.load_input_files_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.load_files)
        QtCore.QObject.connect(self.load_blocks_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.load_blocks_list)
        QtCore.QObject.connect(self.actionClear_Data, QtCore.SIGNAL(_fromUtf8("activated()")), self.clear)
        QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL(_fromUtf8("activated()")), self.about_dialog)
        filename = "./input/!readMe.txt"
        file=open(filename)
        data = file.read()
        self.input_file_help_text.setText(data)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.load_input_files_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.load_files)
        QtCore.QObject.connect(self.select_all_check_box, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.selectAll)
    
    def setup_file_open_dialogs(self):
        self.Ndp_file_edit.setText(self.bii.NinetyInputFile)
        self.ofm_file_edit.setText(self.bii.InjOfmFile)
        self.rgti_file_edit.setText(self.bii.InterpFile)
        self.blocks_file_edit.setText(self.bii.BlockMappingFile)
        self.cells_file_edit.setText(self.bii.CellMappingFile)
        QtCore.QObject.connect(self.Ndp_file_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Ndp_file_dialog)
        QtCore.QObject.connect(self.ofm_file_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ofm_file_dialog)
        QtCore.QObject.connect(self.rgti_file_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.rgti_file_dialog)
        QtCore.QObject.connect(self.cells_file_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cells_file_dialog)
        QtCore.QObject.connect(self.blocks_file_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.blocks_file_dialog)        
        
    def __init__(self):
        self.bii = BlockInjIndex()
        #self.main = Ui_MainWindow()
        self.about_w = Ui_AboutWidget()
        self.inputs_load = 0
        self.blocks_list_for_analysis = []
        #self.setupUi2()
        
    def load_blocks_list(self):
        self.blocks_list_for_analysis = []
        
        return
        
    def clear(self):
        self.__init__()
        self.setup_file_open_dialogs()
        #gc.collect()
        self.statusBar().showMessage('Data cleared')
    
    def load_files(self):
        #QtGui.QMessageBox.about(None, "Message", "start")
        #self.statusBar().showMessage('start to data load')
        if (not QtCore.QFile.exists(self.Ndp_file_edit.text())) | \
            (not QtCore.QFile.exists(self.ofm_file_edit.text())) | \
            (not QtCore.QFile.exists(self.rgti_file_edit.text())) | \
            (not QtCore.QFile.exists(self.blocks_file_edit.text())) | \
            (not QtCore.QFile.exists(self.cells_file_edit.text())) :
            QtGui.QMessageBox.about(None, "Message", "Data loaded\n one of input files doesn't exists")
            #print "bad"
            return
        
        self.bii.NinetyInputFile = self.Ndp_file_edit.text()
        self.bii.InjOfmFile = self.ofm_file_edit.text()
        self.bii.InterpFile = self.rgti_file_edit.text()
        self.bii.BlockMappingFile = self.blocks_file_edit.text()
        self.bii.CellMappingFile = self.cells_file_edit.text()
        print "smthg"
        self.bii.load_data()
        #QtGui.QMessageBox.about(None, "Message", "Data loaded")
        #self.statusBar().showMessage('Data loaded')
        self.create_check_boxes()
        
    def create_check_boxes(self):
        """create dynamycally list of checkboxes from blocks_list"""
        model = QtGui.QStandardItemModel()
        check = QtCore.Qt.Checked
        for n in self.bii.blocks_list :                   
            item = QtGui.QStandardItem(n)
            item.setCheckState(check)
            item.setCheckable(True)
            model.appendRow(item)
        self.listView.setModel(model)
        

    def selectAll(self, state=QtCore.Qt.Checked):
        """Select All layers loaded inside the listView"""
        model = self.listView.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable():
                item.setCheckState(state)
            
    def about_dialog(self):
        about = QtGui.QWidget()
        self.about_w.setupUi(about)
        filename = "about.txt"
        file=open(filename)
        data = file.read()
        self.about_w.about_text.setText(data)
        about.show()
        about.exec_()
    
    def set_connections(self):
        #smthg
        return 0
        
    def Ndp_file_dialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open file')
        self.Ndp_file_edit.setText(filename)
        
    def ofm_file_dialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open file')
        self.ofm_file_edit.setText(filename)
        
    def rgti_file_dialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open file')
        self.rgti_file_edit.setText(filename)
        
    def blocks_file_dialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open file')
        self.blocks_file_edit.setText(filename)
        
    def cells_file_dialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open file')
        self.cells_file_edit.setText(filename)
        
if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = QtGui.QMainWindow()
    mwin = user_interface()
    mwin.setupUi2(form)
    form.show()
    sys.exit(app.exec_())