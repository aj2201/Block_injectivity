# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI/PIR_calc_modified.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(965, 687)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.InputFiles = QtGui.QWidget()
        self.InputFiles.setObjectName(_fromUtf8("InputFiles"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.InputFiles)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.InputFiles)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.rgti_file_edit = QtGui.QLineEdit(self.InputFiles)
        self.rgti_file_edit.setObjectName(_fromUtf8("rgti_file_edit"))
        self.horizontalLayout_2.addWidget(self.rgti_file_edit)
        self.rgti_file_button = QtGui.QPushButton(self.InputFiles)
        self.rgti_file_button.setObjectName(_fromUtf8("rgti_file_button"))
        self.horizontalLayout_2.addWidget(self.rgti_file_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_2 = QtGui.QLabel(self.InputFiles)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.Ndp_file_edit = QtGui.QLineEdit(self.InputFiles)
        self.Ndp_file_edit.setObjectName(_fromUtf8("Ndp_file_edit"))
        self.horizontalLayout_3.addWidget(self.Ndp_file_edit)
        self.Ndp_file_button = QtGui.QPushButton(self.InputFiles)
        self.Ndp_file_button.setObjectName(_fromUtf8("Ndp_file_button"))
        self.horizontalLayout_3.addWidget(self.Ndp_file_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_3 = QtGui.QLabel(self.InputFiles)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.ofm_file_edit = QtGui.QLineEdit(self.InputFiles)
        self.ofm_file_edit.setObjectName(_fromUtf8("ofm_file_edit"))
        self.horizontalLayout_4.addWidget(self.ofm_file_edit)
        self.ofm_file_button = QtGui.QPushButton(self.InputFiles)
        self.ofm_file_button.setObjectName(_fromUtf8("ofm_file_button"))
        self.horizontalLayout_4.addWidget(self.ofm_file_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.label_4 = QtGui.QLabel(self.InputFiles)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.blocks_file_edit = QtGui.QLineEdit(self.InputFiles)
        self.blocks_file_edit.setObjectName(_fromUtf8("blocks_file_edit"))
        self.horizontalLayout_5.addWidget(self.blocks_file_edit)
        self.blocks_file_button = QtGui.QPushButton(self.InputFiles)
        self.blocks_file_button.setObjectName(_fromUtf8("blocks_file_button"))
        self.horizontalLayout_5.addWidget(self.blocks_file_button)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.label_5 = QtGui.QLabel(self.InputFiles)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.cells_file_edit = QtGui.QLineEdit(self.InputFiles)
        self.cells_file_edit.setObjectName(_fromUtf8("cells_file_edit"))
        self.horizontalLayout_6.addWidget(self.cells_file_edit)
        self.cells_file_button = QtGui.QPushButton(self.InputFiles)
        self.cells_file_button.setObjectName(_fromUtf8("cells_file_button"))
        self.horizontalLayout_6.addWidget(self.cells_file_button)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.load_input_files_button = QtGui.QPushButton(self.InputFiles)
        self.load_input_files_button.setObjectName(_fromUtf8("load_input_files_button"))
        self.horizontalLayout_8.addWidget(self.load_input_files_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.input_file_help_text = QtGui.QTextBrowser(self.InputFiles)
        self.input_file_help_text.setObjectName(_fromUtf8("input_file_help_text"))
        self.verticalLayout_3.addWidget(self.input_file_help_text)
        self.tabWidget.addTab(self.InputFiles, _fromUtf8(""))
        self.BlockSelect = QtGui.QWidget()
        self.BlockSelect.setEnabled(True)
        self.BlockSelect.setObjectName(_fromUtf8("BlockSelect"))
        self.verticalLayout_13 = QtGui.QVBoxLayout(self.BlockSelect)
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.label_6 = QtGui.QLabel(self.BlockSelect)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_15.addWidget(self.label_6)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem2)
        self.verticalLayout_13.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.big_blocks_checkBox = QtGui.QCheckBox(self.BlockSelect)
        self.big_blocks_checkBox.setObjectName(_fromUtf8("big_blocks_checkBox"))
        self.horizontalLayout_10.addWidget(self.big_blocks_checkBox)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_7 = QtGui.QLabel(self.BlockSelect)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_7.addWidget(self.label_7)
        self.lineEdit_filter = QtGui.QLineEdit(self.BlockSelect)
        self.lineEdit_filter.setObjectName(_fromUtf8("lineEdit_filter"))
        self.horizontalLayout_7.addWidget(self.lineEdit_filter)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.listView_all_blocks = QtGui.QListView(self.BlockSelect)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listView_all_blocks.setFont(font)
        self.listView_all_blocks.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listView_all_blocks.setObjectName(_fromUtf8("listView_all_blocks"))
        self.verticalLayout_5.addWidget(self.listView_all_blocks)
        self.horizontalLayout_11.addLayout(self.verticalLayout_5)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem4)
        self.pushButton_add_to_list = QtGui.QPushButton(self.BlockSelect)
        self.pushButton_add_to_list.setObjectName(_fromUtf8("pushButton_add_to_list"))
        self.verticalLayout_7.addWidget(self.pushButton_add_to_list)
        self.line = QtGui.QFrame(self.BlockSelect)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_7.addWidget(self.line)
        self.pushButton_remove_from_list = QtGui.QPushButton(self.BlockSelect)
        self.pushButton_remove_from_list.setObjectName(_fromUtf8("pushButton_remove_from_list"))
        self.verticalLayout_7.addWidget(self.pushButton_remove_from_list)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem5)
        self.horizontalLayout_11.addLayout(self.verticalLayout_7)
        self.verticalLayout_12 = QtGui.QVBoxLayout()
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.label_8 = QtGui.QLabel(self.BlockSelect)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_12.addWidget(self.label_8)
        self.listView_for_plotting = QtGui.QListView(self.BlockSelect)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listView_for_plotting.setFont(font)
        self.listView_for_plotting.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listView_for_plotting.setObjectName(_fromUtf8("listView_for_plotting"))
        self.verticalLayout_12.addWidget(self.listView_for_plotting)
        self.horizontalLayout_11.addLayout(self.verticalLayout_12)
        self.verticalLayout_13.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem6)
        self.load_blocks_button = QtGui.QPushButton(self.BlockSelect)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.load_blocks_button.setFont(font)
        self.load_blocks_button.setObjectName(_fromUtf8("load_blocks_button"))
        self.horizontalLayout_13.addWidget(self.load_blocks_button)
        self.verticalLayout_13.addLayout(self.horizontalLayout_13)
        self.tabWidget.addTab(self.BlockSelect, _fromUtf8(""))
        self.OutputPlots = QtGui.QWidget()
        self.OutputPlots.setLocale(QtCore.QLocale(QtCore.QLocale.Russian, QtCore.QLocale.RussianFederation))
        self.OutputPlots.setObjectName(_fromUtf8("OutputPlots"))
        self.gridLayout_2 = QtGui.QGridLayout(self.OutputPlots)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.splitter = QtGui.QSplitter(self.OutputPlots)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.scrollArea = QtGui.QScrollArea(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 274, 575))
        self.scrollAreaWidgetContents_2.setMinimumSize(QtCore.QSize(5, 12))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.plots_select_all = QtGui.QCheckBox(self.scrollAreaWidgetContents_2)
        self.plots_select_all.setObjectName(_fromUtf8("plots_select_all"))
        self.verticalLayout_9.addWidget(self.plots_select_all)
        self.listView_2 = QtGui.QListView(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.listView_2.setFont(font)
        self.listView_2.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listView_2.setObjectName(_fromUtf8("listView_2"))
        self.verticalLayout_9.addWidget(self.listView_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.matplotlibwidget = MatplotlibWidget(self.layoutWidget)
        self.matplotlibwidget.setObjectName(_fromUtf8("matplotlibwidget"))
        self.verticalLayout_6.addWidget(self.matplotlibwidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox_prod_skin_plot = QtGui.QCheckBox(self.layoutWidget)
        self.checkBox_prod_skin_plot.setObjectName(_fromUtf8("checkBox_prod_skin_plot"))
        self.horizontalLayout.addWidget(self.checkBox_prod_skin_plot)
        self.checkBox_inj_skin_plot = QtGui.QCheckBox(self.layoutWidget)
        self.checkBox_inj_skin_plot.setObjectName(_fromUtf8("checkBox_inj_skin_plot"))
        self.horizontalLayout.addWidget(self.checkBox_inj_skin_plot)
        self.checkBox_pi_ratio_plot = QtGui.QCheckBox(self.layoutWidget)
        self.checkBox_pi_ratio_plot.setObjectName(_fromUtf8("checkBox_pi_ratio_plot"))
        self.horizontalLayout.addWidget(self.checkBox_pi_ratio_plot)
        spacerItem7 = QtGui.QSpacerItem(54, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.plot_update_button = QtGui.QPushButton(self.layoutWidget)
        self.plot_update_button.setObjectName(_fromUtf8("plot_update_button"))
        self.horizontalLayout.addWidget(self.plot_update_button)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.clear_plot_button = QtGui.QPushButton(self.layoutWidget)
        self.clear_plot_button.setObjectName(_fromUtf8("clear_plot_button"))
        self.horizontalLayout.addWidget(self.clear_plot_button)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        self.pushButton_save_plots = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_save_plots.setObjectName(_fromUtf8("pushButton_save_plots"))
        self.horizontalLayout.addWidget(self.pushButton_save_plots)
        spacerItem10 = QtGui.QSpacerItem(32, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem10)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.OutputPlots, _fromUtf8(""))
        self.table_out = QtGui.QWidget()
        self.table_out.setEnabled(True)
        self.table_out.setObjectName(_fromUtf8("table_out"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.table_out)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.toolBox = QtGui.QToolBox(self.table_out)
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.injectors_skin = QtGui.QWidget()
        self.injectors_skin.setGeometry(QtCore.QRect(0, 0, 925, 483))
        self.injectors_skin.setObjectName(_fromUtf8("injectors_skin"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.injectors_skin)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.tableView_inj_skin = QtGui.QTableView(self.injectors_skin)
        self.tableView_inj_skin.setSortingEnabled(True)
        self.tableView_inj_skin.setObjectName(_fromUtf8("tableView_inj_skin"))
        self.verticalLayout_8.addWidget(self.tableView_inj_skin)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem11)
        self.pushButton_save_iskin_table_to_file = QtGui.QPushButton(self.injectors_skin)
        self.pushButton_save_iskin_table_to_file.setObjectName(_fromUtf8("pushButton_save_iskin_table_to_file"))
        self.horizontalLayout_12.addWidget(self.pushButton_save_iskin_table_to_file)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.toolBox.addItem(self.injectors_skin, _fromUtf8(""))
        self.producers_skin = QtGui.QWidget()
        self.producers_skin.setGeometry(QtCore.QRect(0, 0, 108, 115))
        self.producers_skin.setObjectName(_fromUtf8("producers_skin"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.producers_skin)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.tableView_prod_skin = QtGui.QTableView(self.producers_skin)
        self.tableView_prod_skin.setSortingEnabled(True)
        self.tableView_prod_skin.setObjectName(_fromUtf8("tableView_prod_skin"))
        self.verticalLayout_10.addWidget(self.tableView_prod_skin)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        spacerItem12 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem12)
        self.pushButton_save_pskin_table_to_file = QtGui.QPushButton(self.producers_skin)
        self.pushButton_save_pskin_table_to_file.setObjectName(_fromUtf8("pushButton_save_pskin_table_to_file"))
        self.horizontalLayout_9.addWidget(self.pushButton_save_pskin_table_to_file)
        self.verticalLayout_10.addLayout(self.horizontalLayout_9)
        self.toolBox.addItem(self.producers_skin, _fromUtf8(""))
        self.pi_ratio = QtGui.QWidget()
        self.pi_ratio.setGeometry(QtCore.QRect(0, 0, 108, 115))
        self.pi_ratio.setObjectName(_fromUtf8("pi_ratio"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.pi_ratio)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.tableView_pi_ratio = QtGui.QTableView(self.pi_ratio)
        self.tableView_pi_ratio.setSortingEnabled(True)
        self.tableView_pi_ratio.setObjectName(_fromUtf8("tableView_pi_ratio"))
        self.verticalLayout_11.addWidget(self.tableView_pi_ratio)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        spacerItem13 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem13)
        self.pushButton_save_pir_table_to_file = QtGui.QPushButton(self.pi_ratio)
        self.pushButton_save_pir_table_to_file.setObjectName(_fromUtf8("pushButton_save_pir_table_to_file"))
        self.horizontalLayout_14.addWidget(self.pushButton_save_pir_table_to_file)
        self.verticalLayout_11.addLayout(self.horizontalLayout_14)
        self.toolBox.addItem(self.pi_ratio, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.toolBox)
        self.tabWidget.addTab(self.table_out, _fromUtf8(""))
        self.verticalLayout_4.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 965, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.menubar.setFont(font)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuHelp_2 = QtGui.QMenu(self.menubar)
        self.menuHelp_2.setObjectName(_fromUtf8("menuHelp_2"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionClear_Data = QtGui.QAction(MainWindow)
        self.actionClear_Data.setObjectName(_fromUtf8("actionClear_Data"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionClear_Data)
        self.menuHelp.addAction(self.actionExit)
        self.menuHelp_2.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuHelp_2.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.toolBox.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Block Injectivity Calculation", None))
        self.label.setText(_translate("MainWindow", "RGTI file                                     ", None))
        self.rgti_file_button.setText(_translate("MainWindow", "...", None))
        self.label_2.setText(_translate("MainWindow", "90dp pressures an PIs", None))
        self.Ndp_file_button.setText(_translate("MainWindow", "...", None))
        self.label_3.setText(_translate("MainWindow", "OFm report of injection and BHP", None))
        self.ofm_file_button.setText(_translate("MainWindow", "...", None))
        self.label_4.setText(_translate("MainWindow", "Blocks mapping", None))
        self.blocks_file_button.setText(_translate("MainWindow", "...", None))
        self.label_5.setText(_translate("MainWindow", "Cells mapping", None))
        self.cells_file_button.setText(_translate("MainWindow", "...", None))
        self.load_input_files_button.setText(_translate("MainWindow", "Load input files", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.InputFiles), _translate("MainWindow", "Input files", None))
        self.label_6.setText(_translate("MainWindow", "Select  blocks for analysis", None))
        self.big_blocks_checkBox.setText(_translate("MainWindow", "Display blocks only", None))
        self.label_7.setText(_translate("MainWindow", "Filter:", None))
        self.pushButton_add_to_list.setText(_translate("MainWindow", "add>>", None))
        self.pushButton_remove_from_list.setText(_translate("MainWindow", "<<delete", None))
        self.label_8.setText(_translate("MainWindow", "Blocks for analysis", None))
        self.load_blocks_button.setText(_translate("MainWindow", "Load Blocks List", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.BlockSelect), _translate("MainWindow", "Blocks/Patterns select", None))
        self.plots_select_all.setText(_translate("MainWindow", "Select All", None))
        self.checkBox_prod_skin_plot.setText(_translate("MainWindow", "P Skin", None))
        self.checkBox_inj_skin_plot.setText(_translate("MainWindow", "I skin", None))
        self.checkBox_pi_ratio_plot.setText(_translate("MainWindow", "P/I ratio", None))
        self.plot_update_button.setText(_translate("MainWindow", "Plot", None))
        self.clear_plot_button.setText(_translate("MainWindow", "Clear", None))
        self.pushButton_save_plots.setText(_translate("MainWindow", "Save all", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.OutputPlots), _translate("MainWindow", "Plots", None))
        self.pushButton_save_iskin_table_to_file.setText(_translate("MainWindow", "Save to file", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.injectors_skin), _translate("MainWindow", "Injection skin", None))
        self.pushButton_save_pskin_table_to_file.setText(_translate("MainWindow", "Save to file", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.producers_skin), _translate("MainWindow", "Producing skin", None))
        self.pushButton_save_pir_table_to_file.setText(_translate("MainWindow", "Save to file", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.pi_ratio), _translate("MainWindow", "Productivity Injectivity ratio", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.table_out), _translate("MainWindow", "Table Output", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Main", None))
        self.menuHelp_2.setTitle(_translate("MainWindow", "Help", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionClear_Data.setText(_translate("MainWindow", "Clear Data", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

from matplotlibwidget import MatplotlibWidget
