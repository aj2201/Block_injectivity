# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'save_pics.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_PlotsSaveDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        super(Ui_PlotsSaveDialog, self).__init__(parent)
        self.setupUi()
        
    def setupUi(self, PlotsSaveDialog=None):
        #if PlotsSaveDialog==None: PlotsSaveDialog=QtGui.QDialog():
        PlotsSaveDialog = self
        PlotsSaveDialog.setObjectName(_fromUtf8("PlotsSaveDialog"))
        PlotsSaveDialog.resize(387, 181)
        self.verticalLayout_4 = QtGui.QVBoxLayout(PlotsSaveDialog)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(PlotsSaveDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_destination_folder = QtGui.QLineEdit(PlotsSaveDialog)
        self.lineEdit_destination_folder.setObjectName(_fromUtf8("lineEdit_destination_folder"))
        self.horizontalLayout.addWidget(self.lineEdit_destination_folder)
        self.pushButton_destiantion_folder = QtGui.QPushButton(PlotsSaveDialog)
        self.pushButton_destiantion_folder.setObjectName(_fromUtf8("pushButton_destiantion_folder"))
        self.horizontalLayout.addWidget(self.pushButton_destiantion_folder)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(PlotsSaveDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.lineEdit_max_limit = QtGui.QLineEdit(PlotsSaveDialog)
        self.lineEdit_max_limit.setObjectName(_fromUtf8("lineEdit_max_limit"))
        self.verticalLayout_2.addWidget(self.lineEdit_max_limit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_3 = QtGui.QLabel(PlotsSaveDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.lineEdit_min_limit = QtGui.QLineEdit(PlotsSaveDialog)
        self.lineEdit_min_limit.setObjectName(_fromUtf8("lineEdit_min_limit"))
        self.verticalLayout_3.addWidget(self.lineEdit_min_limit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.checkBox_prod_skin_plot = QtGui.QCheckBox(PlotsSaveDialog)
        self.checkBox_prod_skin_plot.setObjectName(_fromUtf8("checkBox_prod_skin_plot"))
        self.horizontalLayout_3.addWidget(self.checkBox_prod_skin_plot)
        self.checkBox_inj_skin_plot = QtGui.QCheckBox(PlotsSaveDialog)
        self.checkBox_inj_skin_plot.setObjectName(_fromUtf8("checkBox_inj_skin_plot"))
        self.horizontalLayout_3.addWidget(self.checkBox_inj_skin_plot)
        self.checkBox_pi_ratio_plot = QtGui.QCheckBox(PlotsSaveDialog)
        self.checkBox_pi_ratio_plot.setObjectName(_fromUtf8("checkBox_pi_ratio_plot"))
        self.horizontalLayout_3.addWidget(self.checkBox_pi_ratio_plot)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(PlotsSaveDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_4.addWidget(self.buttonBox)
        self.lineEdit_destination_folder.setText("./out")
        self.retranslateUi(PlotsSaveDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PlotsSaveDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PlotsSaveDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PlotsSaveDialog)
        QtCore.QObject.connect( self.pushButton_destiantion_folder, QtCore.SIGNAL(_fromUtf8("clicked()")), self.path_file_dialog)
    
    def path_file_dialog(self):
        the_path = QtGui.QFileDialog.getExistingDirectory(None, 'Select directory')
        self.lineEdit_destination_folder.setText(str(the_path))
        
    def retranslateUi(self, PlotsSaveDialog):
        PlotsSaveDialog.setWindowTitle(_translate("PlotsSaveDialog", "Save plots", None))
        self.label.setText(_translate("PlotsSaveDialog", "Destiantion folder", None))
        self.pushButton_destiantion_folder.setText(_translate("PlotsSaveDialog", "...", None))
        self.label_2.setText(_translate("PlotsSaveDialog", "Max limit (enter \"-\" to autoscale)  ", None))
        self.label_3.setText(_translate("PlotsSaveDialog", "Min limit (enter \"-\" to autoscale)  ", None))
        self.checkBox_prod_skin_plot.setText(_translate("PlotsSaveDialog", "P Skin", None))
        self.checkBox_inj_skin_plot.setText(_translate("PlotsSaveDialog", "I skin", None))
        self.checkBox_pi_ratio_plot.setText(_translate("PlotsSaveDialog", "P/I ratio", None))

    @staticmethod
    def getValues(parent=None):
        #import pdb; pdb.set_trace()
        dialog = Ui_PlotsSaveDialog()
        #dialog.setupUi()
        result = dialog.exec_()
        destination_path = str(dialog.lineEdit_destination_folder.text())
        iskin_plt = dialog.checkBox_inj_skin_plot.checkState()==QtCore.Qt.Checked
        pskin_plt = dialog.checkBox_prod_skin_plot.checkState() ==QtCore.Qt.Checked
        pi_ratio_plot =dialog.checkBox_pi_ratio_plot.checkState()==QtCore.Qt.Checked
        min_limit = str(dialog.lineEdit_min_limit.text())
        max_limit = str(dialog.lineEdit_max_limit.text())
        return (destination_path, iskin_plt, pskin_plt, pi_ratio_plot, min_limit, max_limit, result==QtGui.QDialog.Accepted)
