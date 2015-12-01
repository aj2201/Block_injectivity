# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 17:18:52 2015

@author: Aygul.Ibatullina
!For exe compiling pyinsatller is used (version 3.1.dev0)

"""
import sys
import operator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PyQt4 import QtCore
from PyQt4 import  QtGui
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

from ProdInjRatioCalc import ProdInjRatioCalc
from Ui_AboutWidget import Ui_AboutWidget
from Ui_MainWindow2 import Ui_MainWindow
from Ui_PlotsSaveDialog import Ui_PlotsSaveDialog

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

class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None
        
    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.mydata = sorted(self.mydata,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mydata.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))


class NumberSortModel(QtGui.QSortFilterProxyModel):

    def lessThan(self, left, right):
    
        lvalue = left.data().toDouble()[0]
        rvalue = right.data().toDouble()[0]
        return lvalue < rvalue  

     
class UserInterface(Ui_MainWindow):
    def __init__(self):
        self.pir_calc = ProdInjRatioCalc()
        #self.main = Ui_MainWindow()
        self.about_w = Ui_AboutWidget()
        self.inputs_load = 0
        self.blocks_list_for_analysis = []
        
    def setupUi2(self, MainWindow):
        self.setupUi(MainWindow)
        self.object = MainWindow
        #self.statusbar = QtGui.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setup_connections()
        self.setup_file_open_dialogs()
        #QtCore.QObject.connect(self.start_time_edit, QtCore.SIGNAL(_fromUtf8("dateChanged(QDate)")), self.menubar.raise_)
        filename = "./input/!readMe.txt"
        try:
            file_readMe=open(filename)
            data = file_readMe.read()
        except IOError:
            data = "!readMe.txt file not found"
                        
        #data = file_readMe.read()
        
        data = data.decode("utf-8")
        self.input_file_help_text.setText(data)
        self.tabWidget.setCurrentIndex(0)
        self.navi_toolbar = NavigationToolbar(self.matplotlibwidget, self.OutputPlots)
        self.verticalLayout_6.addChildWidget(self.navi_toolbar)
        self.object.statusBar().showMessage('Ready')
        self.big_blocks_checkBox.setChecked(True)
        #self.tableView_snapshot = DataFrameWidget()
        
    def setup_connections(self):
        QtCore.QObject.connect(self.load_input_files_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.load_input_files)
        QtCore.QObject.connect(self.load_blocks_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.load_blocks_list)
        QtCore.QObject.connect(self.actionClear_Data, QtCore.SIGNAL(_fromUtf8("activated()")), self.clear)
        QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL(_fromUtf8("activated()")), self.about_dialog)
        QtCore.QObject.connect(self.load_input_files_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.load_input_files)
        QtCore.QObject.connect(self.plots_select_all, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.plot_select_all_function)
        QtCore.QObject.connect(self.plot_update_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.plot_new)
        QtCore.QObject.connect(self.clear_plot_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clear_plot)
        QtCore.QObject.connect(self.pushButton_save_plots, QtCore.SIGNAL(_fromUtf8("clicked()")), self.save_plots_to_file)
        QtCore.QObject.connect(self.big_blocks_checkBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),self.big_blocks_display)
        QtCore.QObject.connect(self.pushButton_save_pir_table_to_file, QtCore.SIGNAL(_fromUtf8("clicked()")), self.save_pir_table_to_file)
        QtCore.QObject.connect(self.pushButton_save_iskin_table_to_file, QtCore.SIGNAL(_fromUtf8("clicked()")), self.save_iskin_table_to_file)
        QtCore.QObject.connect(self.pushButton_save_pskin_table_to_file, QtCore.SIGNAL(_fromUtf8("clicked()")), self.save_pskin_table_to_file)
        
        QtCore.QObject.connect(self.pushButton_add_to_list, QtCore.SIGNAL(_fromUtf8("clicked()")), self.add_to_plotting_list)
        QtCore.QObject.connect(self.pushButton_remove_from_list, QtCore.SIGNAL(_fromUtf8("clicked()")), self.remove_from_plotting_list)
        QtCore.QObject.connect(self.lineEdit_filter, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.filter_all_blocks_list)
    
    def setup_file_open_dialogs(self):
        self.Ndp_file_edit.setText(self.pir_calc.NinetyInputFile)
        self.ofm_file_edit.setText(self.pir_calc.InjOfmFile)
        self.rgti_file_edit.setText(self.pir_calc.InterpFile)
        self.blocks_file_edit.setText(self.pir_calc.BlockMappingFile)
        self.cells_file_edit.setText(self.pir_calc.CellMappingFile)
        QtCore.QObject.connect(self.Ndp_file_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Ndp_file_dialog)
        QtCore.QObject.connect(self.ofm_file_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ofm_file_dialog)
        QtCore.QObject.connect(self.rgti_file_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.rgti_file_dialog)
        QtCore.QObject.connect(self.cells_file_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cells_file_dialog)
        QtCore.QObject.connect(self.blocks_file_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.blocks_file_dialog)        
        
    def add_to_plotting_list(self):
        model_to = self.listView_for_plotting.model()
        #model_from = self.listView_all_blocks.model()
        rows= self.listView_all_blocks.selectionModel().selectedRows()
        for row in rows:
            item = QtGui.QStandardItem(row.data())
            if len(model_to.findItems(item.text())) ==0:
                model_to.appendRow(item)
        model_to.sort()
        self.listView_for_plotting.update()
        return
        
    def remove_from_plotting_list(self):
        model = self.listView_for_plotting.model()
        indxs= self.listView_for_plotting.selectedIndexes()        
        rows = []
        for index in indxs:
            rows.append(index.row())
        rows.sort(reverse=True)
        for row in rows: 
            model.removeRow(row)
        self.listView_for_plotting.update()        
    
    def filter_all_blocks_list(self, filter_text=""):
        if self.big_blocks_checkBox.isChecked()==True:
            list_for_display = list(set(self.pir_calc.blocks_list) - set(self.pir_calc.cells_list))
        else:
            list_for_display = self.pir_calc.blocks_list
        list_for_display.sort()
        filtered_list = filter(lambda t: filter_text in t, list_for_display)
        self.update_all_blocks_list(filtered_list)
        return
        
        
    def load_tables(self):
        the_list = []
        #extract list from listView2 to plot 
        model = self.listView_for_plotting.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            #if item.checkState():
            the_list.append(item.text())
        #to avoid problems with interacting of pandas and qtstring
        the_list = map(str, the_list)
        #i skin
        self.table_load(the_list, self.pir_calc.block_inj_skin_table, self.tableView_inj_skin)
        self.table_load(the_list, self.pir_calc.block_prod_skin_table, self.tableView_prod_skin)
        self.table_load(the_list, self.pir_calc.prod_inj_ratio_table, self.tableView_pi_ratio)
        
        
        
    def table_load(self, the_list, source_table, tableView):
        #import pdb; pdb.set_trace()
        df = source_table[the_list].T.copy()
        #df.values = map(np.round,df.values, 3)
        df.columns = map(lambda x: x.strftime('%d-%m-%Y'), df.columns)
        df.reset_index(level=0, inplace=True)        
        model = PandasModel(df)
        #import pdb; pdb.set_trace()
        proxy = QtGui.QSortFilterProxyModel() #NumberSortModel()
        proxy.setSourceModel(model)
        tableView.setModel(proxy)
        tableView.setSortingEnabled(True)
        #print proxy.columnCount(), model.columnCount()
        tableView.update()
        return
     
    def save_pir_table_to_file(self):
         self.save_table_to_file("PIR")
         
    def save_iskin_table_to_file(self):
        self.save_table_to_file("Iskin")
        
    def save_pskin_table_to_file(self):
        self.save_table_to_file("Pskin")
     
    def save_table_to_file(self, variable):
        the_list = []
        #extract list from listView2 to plot 
        model = self.listView_for_plotting.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            #if item.checkState():
            the_list.append(item.text())
        #to avoid problems with interacting of pandas and qtstring
        the_list = map(str, the_list)
        filename,the_filter =QtGui.QFileDialog.getSaveFileNameAndFilter(None, "Save as", ".","*.csv" )
        if variable=="PIR": self.pir_calc.prod_inj_ratio_table[the_list].to_csv(filename, sep="\t", date_format="%d.%m.%Y")
        if variable=="Pskin": self.pir_calc.block_prod_skin_table[the_list].to_csv(filename, sep="\t", date_format="%d.%m.%Y")
        if variable=="Iskin": self.pir_calc.block_inj_skin_table[the_list].to_csv(filename, sep="\t", date_format="%d.%m.%Y")
        
    def save_plots_to_file(self):
        destination_path, iskin_plt, pskin_plt, pi_ratio_plot, min_limit, max_limit, result = Ui_PlotsSaveDialog.getValues()
        if result==False: return
        i_skin_plot_flag = iskin_plt
        p_skin_plot_flag = pskin_plt
        pir_plot_flag = pi_ratio_plot
        the_list = []
        #extract list from listView2 to plot 
        model = self.listView_2.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.checkState():
                the_list.append(item.text())
        #to avoid problems with interacting of pandas and qtstring
        the_list = map(str, the_list)
        #to calc layot of subplots
        #plots_number = float(len(the_list))        
        plt.ioff()
        try:
            min_limit=int(min_limit)
        except ValueError:
            min_limit=None
        try:
            max_limit=int(max_limit)
        except ValueError:
            max_limit=None
        for block in the_list:
            #plotting each block on separate subplot
            fig = plt.figure(figsize=(10, 6), dpi=80)
            axes = fig.gca()
            df_iskin = self.pir_calc.block_inj_skin_table[block]
            df_pskin = self.pir_calc.block_prod_skin_table[block]
            df_pir = self.pir_calc.prod_inj_ratio_table[block]
            df_iskin.name = "skin(i)"
            df_pskin.name = "skin(p)"
            df_pir.name = "P/I"
            #sub_axes = self.matplotlibwidget.figure.add_subplot(v,h,i, sharey=first_axes, sharex=first_axes)
            if i_skin_plot_flag: pd.DataFrame(df_iskin).plot(ax=axes, color="blue", ylim=(min_limit, max_limit))
            if p_skin_plot_flag: pd.DataFrame(df_pskin).plot(ax=axes, color="green", ylim=(min_limit, max_limit))
            if pir_plot_flag: pd.DataFrame(df_pir).plot(ax=axes, color="red", ylim=(min_limit, max_limit))
            filename = destination_path+"/"+block+".png"
            fig.suptitle(block,  fontsize=14, fontweight='bold')
            fig.savefig(filename,dpi=200, transparent=False)
    
    def clear_plot(self):
        self.object.statusBar().showMessage('Plots area cleared')
        self.matplotlibwidget.figure.clear()
        #df = pd.DataFrame([0,0])
        #df.plot(ax=self.matplotlibwidget.axes)
        self.matplotlibwidget.draw()
        #self.matplotlibwidget.update()
        
        
    def plot(self):
        self.matplotlibwidget.axes.clear()
        the_list = []
        #extract list to plot from form
        model = self.listView_2.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.checkState():
                the_list.append(item.text())
        #to avoid problems with interacting of pandas as qtstring
        the_list = map(str, the_list)
        if len(the_list)>0:
            df_iskin = self.pir_calc.block_inj_skin_table[the_list]
            #df_pskin = self.pir_calc.block_prod_skin_table[the_list]
            #df_pi_ratio = = self.pir_calc.p[the_list]
        else: return
        #to calculate how plot subplots
        plots_number = float(len(df_iskin.columns))
        v = int(np.ceil(plots_number ** 0.5))
        h = int(np.ceil(plots_number / v ))
        if plots_number < 4:
            v = int(np.min([3., plots_number]))
            h = 1
        if plots_number > 1:
            df_iskin.plot(subplots=True, layout=(v,h), ax=self.matplotlibwidget.axes)
        else:
            #df_iskin.plot(ax=self.matplotlibwidget.axes)
            #self.matplotlibwidget.figure.axes
            print type(df_iskin)
            pd.DataFrame(df_iskin).plot(ax=self.matplotlibwidget.axes)
            #self.matplotlibwidget.axes.plot(df_iskin.index, df_iskin.values)
            
        self.matplotlibwidget.draw()
        self.object.statusBar().showMessage('Plots ')
        
        
    def plot_new(self):
        self.clear_plot()
        i_skin_plot_flag = (self.checkBox_inj_skin_plot.checkState() ==QtCore.Qt.Checked)
        p_skin_plot_flag = (self.checkBox_prod_skin_plot.checkState() ==QtCore.Qt.Checked)
        pir_plot_flag = (self.checkBox_pi_ratio_plot.checkState() ==QtCore.Qt.Checked)
        the_list = []
        #extract list from listView2 to plot 
        model = self.listView_2.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.checkState():
                the_list.append(item.text())
        #to avoid problems with interacting of pandas and qtstring
        the_list = map(str, the_list)
        #to calc layot of subplots
        plots_number = float(len(the_list))
        v = int(np.ceil(plots_number ** 0.5))
        h = int(np.ceil(plots_number / v ))
        if plots_number < 4:
            v = int(np.min([3., plots_number]))
            h = 1
        i=1
        first_axes = self.matplotlibwidget.figure.add_subplot(v,h,i)
        for block in the_list:
            #plotting each block on separate subplot
            df_iskin = self.pir_calc.block_inj_skin_table[block]
            df_pskin = self.pir_calc.block_prod_skin_table[block]
            df_pir = self.pir_calc.prod_inj_ratio_table[block]
            df_iskin.name = block+" skin(i)"
            df_pskin.name = block+" skin(p)"
            df_pir.name = block+" P/I"
            sub_axes = self.matplotlibwidget.figure.add_subplot(v,h,i, sharey=first_axes, sharex=first_axes)
            if i_skin_plot_flag: pd.DataFrame(df_iskin).plot(ax=sub_axes,color="blue")
            if p_skin_plot_flag: pd.DataFrame(df_pskin).plot(ax=sub_axes,color="green")
            if pir_plot_flag: pd.DataFrame(df_pir).plot(ax=sub_axes,color="red")
            i = i + 1
        self.matplotlibwidget.figure.tight_layout(pad=0.08, h_pad=0.2, w_pad=0.2)
        self.matplotlibwidget.draw()
        
    def add_plot_list(self):
        """create dynamycally list of checkboxes from blocks_list_for_analysis"""
        model = QtGui.QStandardItemModel()
        check = QtCore.Qt.Unchecked
        for n in self.blocks_list_for_analysis :                   
            item = QtGui.QStandardItem(n)
            item.setCheckState(check)
            item.setCheckable(True)
            model.appendRow(item)
        self.listView_2.setModel(model)
        #self.tabWidget.currentChanged(2)
        
    def plot_select_all_function(self, state=QtCore.Qt.Checked):
        """Select All layers loaded inside the listView"""
        model = self.listView_2.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable():
                item.setCheckState(state)
    
    def load_blocks_list(self):
        self.object.statusBar().showMessage('blocks list loading')
        self.listView_2.setModel(QtGui.QStandardItemModel())
        the_list = []
        model = self.listView_for_plotting.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            #if item.checkState():
            the_list.append(item.text())
        self.blocks_list_for_analysis = map(str,the_list)
        #self.pir_calc.pi_ratio_calc(self.blocks_list_for_analysis)
        self.object.statusBar().showMessage('blocks list loaded')
        self.add_plot_list()
        self.load_tables()
        self.object.statusBar().showMessage('blocks list loaded.')
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget.update()
             
    def clear(self):
        #TODO: clear all tabs
        self.__init__()
        self.setup_file_open_dialogs()
        self.listView_all_blocks.setModel(QtGui.QStandardItemModel())
        self.listView_for_plotting.setModel(QtGui.QStandardItemModel())
        self.clear_plot()
        self.listView_2.setModel(QtGui.QStandardItemModel())
        #gc.collect()
        self.object.statusBar().showMessage('Data cleared')
        emptymodel = QtGui.QStandardItemModel()
        self.tableView_inj_skin.setModel(emptymodel)
        self.tableView_pi_ratio.setModel(emptymodel)
        self.tableView_prod_skin.setModel(emptymodel)
        self.tableView_inj_skin.update()
        self.tableView_pi_ratio.update()
        self.tableView_prod_skin.update()
        
    
    def load_input_files(self):
        self.object.statusBar().showMessage('data loading, it takes minute')
        #QtGui.QMessageBox.about(None, "Message", "start")
        #self.statusBar.showMessage('start to data load')
        
        if (not QtCore.QFile.exists(self.Ndp_file_edit.text())) | \
            (not QtCore.QFile.exists(self.ofm_file_edit.text())) | \
            (not QtCore.QFile.exists(self.rgti_file_edit.text())) | \
            (not QtCore.QFile.exists(self.blocks_file_edit.text())) | \
            (not QtCore.QFile.exists(self.cells_file_edit.text())) :
            QtGui.QMessageBox.about(None, "Message", "Data not loaded\n one of input files doesn't exists")
            self.object.statusBar().showMessage('Data not loaded one of input files doesn\'t exists')
            return
        
        self.pir_calc.NinetyInputFile = str(self.Ndp_file_edit.text())
        self.pir_calc.InjOfmFile = str(self.ofm_file_edit.text())
        self.pir_calc.InterpFile = str(self.rgti_file_edit.text())
        self.pir_calc.BlockMappingFile = str(self.blocks_file_edit.text())
        self.pir_calc.CellMappingFile = str(self.cells_file_edit.text())
        self.pir_calc.load_data()
        self.create_all_blocks_list()      
        self.listView_for_plotting.setModel(QtGui.QStandardItemModel())
        self.object.statusBar().showMessage('Calculating.')
        self.pir_calc.pi_ratio_calc()
        self.object.statusBar().showMessage('Data loaded.')
        self.object.statusBar().showMessage('Data loaded.')
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget.update()
     
    def big_blocks_display(self, state=QtCore.Qt.Checked):
        self.create_all_blocks_list(state)
        
    def create_all_blocks_list(self, state=QtCore.Qt.Checked):
        """create dynamycally list of checkboxes from blocks_list"""
        #import pdb; pdb.set_trace()
        #check = QtCore.Qt.Unchecked
        if state==QtCore.Qt.Checked:
            list_for_display = list(set(self.pir_calc.blocks_list) - set(self.pir_calc.cells_list))
        else:
            list_for_display = self.pir_calc.blocks_list
        list_for_display.sort()
        self.update_all_blocks_list(list_for_display)
        
        
    def update_all_blocks_list(self, list_for_display=None):
        model = QtGui.QStandardItemModel()
        if list_for_display==None:
            self.create_all_blocks_list()
            return
        for n in list_for_display:                   
            item = QtGui.QStandardItem(n)
            #item.setCheckState(check)
            #item.setCheckable(True)
            model.appendRow(item)
        self.listView_all_blocks.setModel(model)

            
    def about_dialog(self):
        about = QtGui.QWidget()
        self.about_w.setupUi(about)
        filename = "about.txt"
        file=open(filename)
        data = file.read()
        self.about_w.about_text.setText(data)
        about.show()
        about.exec_()
           
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
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique")) # setting the style
    
    form = QtGui.QMainWindow()
    mwin = UserInterface()
    mwin.setupUi2(form)
    form.show()
    form.setFocus()
    sys.exit(app.exec_())