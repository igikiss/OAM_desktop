from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QMainWindow, QAction, qApp, QTextEdit, QLabel, QGridLayout, QWidget, QFileDialog, QFrame, QComboBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QIcon, QFont, QPixmap, QCursor
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import numpy as np
import pyqtgraph as pg
import sys
from datetime import timedelta
import time

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = ("OAM Desktop")
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.width = self.screen.width()
        self.height = self.screen.height()
        self.top = self.screen.height()
        self.left = self.screen.width()
        self.setGeometry(0, 0, self.width, self.height)
        self.InitWindow()
        self.showMaximized()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        
        self.label = QLabel(self)
        self.label_1 = QLabel('VAPOTHERM OAM VIEWER', self)
        self.label_1.setFont(QFont('Arial', 40, QFont.Bold))
        self.label_1.resize(600, 50)
        self.label_1.setStyleSheet("color: rgb(30, 195, 225);")
        self.label_1.move(700, 50)

        self.l_button = QPushButton('Load File', self)
        self.l_button.move(50, 150)
        self.l_button.resize(200, 50)
        self.l_button.setFont(QFont('Arial', 20, QFont.Bold))
        self.l_button.setStyleSheet("background-color: rgb(30, 195, 225);")
        self.l_button.clicked.connect(self.load_file)
        self.l_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.pdf_button = QPushButton('Export PDF', self)
        self.pdf_button.move(50, 200)
        self.pdf_button.resize(200, 50)
        self.pdf_button.setFont(QFont('Arial', 20, QFont.Bold))
        self.pdf_button.setStyleSheet("background-color: rgb(30, 195, 225);")
        #self.pdf_button.clicked.connect(self.export_pdf)
        self.pdf_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.bar_plot_1 = pg.PlotWidget(self)
        self.bar_plot_1.move(300, 150)
        self.bar_plot_1.resize(300, 300)
        self.bar_plot_1.setBackground('w')  
        self.bar_plot_1.setLabel('left', 'Temperature', units='°C')
        self.bar_plot_1.setLabel('bottom', 'Time', units='s')
        self.bar_plot_1.showGrid(x=True, y=True)
        self.bar_plot_1.setRange(xRange=[0, 100], yRange=[0, 100], padding=0)
        self.bar_plot_1.setMouseEnabled(x=False, y=False)
        self.bar_plot_1.setMenuEnabled(False)
        self.bar_plot_1.setLogMode(x=False, y=False)
        self.bar_plot_1.setClipToView(True)
        self.bar_plot_1.setAntialiasing(True)
        self.bar_plot_1.setDownsampling(mode='peak')
        self.bar_plot_1.setLimits(xMin=0, xMax=100, yMin=0, yMax=100)

        self.bar_plot_2 = pg.PlotWidget(self)
        self.bar_plot_2.move(650, 150)
        self.bar_plot_2.resize(300, 300)
        self.bar_plot_2.setBackground('w')
        self.bar_plot_2.setLabel('left', 'Temperature', units='°C')
        self.bar_plot_2.setLabel('bottom', 'Time', units='s')
        self.bar_plot_2.showGrid(x=True, y=True)
        self.bar_plot_2.setRange(xRange=[0, 100], yRange=[0, 100], padding=0)
        self.bar_plot_2.setMouseEnabled(x=False, y=False)
        self.bar_plot_2.setMenuEnabled(False)
        self.bar_plot_2.setLogMode(x=False, y=False)
        self.bar_plot_2.setClipToView(True)
        self.bar_plot_2.setAntialiasing(True)
        self.bar_plot_2.setDownsampling(mode='peak')
        self.bar_plot_2.setLimits(xMin=0, xMax=100, yMin=0, yMax=100)

        self.bar_plot_3 = pg.PlotWidget(self)
        self.bar_plot_3.move(1000, 150)
        self.bar_plot_3.resize(300, 300)
        self.bar_plot_3.setBackground('w')
        self.bar_plot_3.setLabel('left', 'Temperature', units='°C')
        self.bar_plot_3.setLabel('bottom', 'Time', units='s')
        self.bar_plot_3.showGrid(x=True, y=True)
        self.bar_plot_3.setRange(xRange=[0, 100], yRange=[0, 100], padding=0)
        self.bar_plot_3.setMouseEnabled(x=False, y=False)
        self.bar_plot_3.setMenuEnabled(False)
        self.bar_plot_3.setLogMode(x=False, y=False)
        self.bar_plot_3.setClipToView(True)
        self.bar_plot_3.setAntialiasing(True)
        self.bar_plot_3.setDownsampling(mode='peak')
        self.bar_plot_3.setLimits(xMin=0, xMax=100, yMin=0, yMax=100)

        #create a table widget with 5 rows and 2 columns and size 300x300
        self.tableWidget = QTableWidget(5, 2, self)
        self.tableWidget.move(1350, 150)
        self.tableWidget.resize(300, 300)
        self.tableWidget.setHorizontalHeaderLabels(['Time', 'Temperature'])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setShowGrid(True)
        #self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: rgb(30, 195, 225);}")
        self.tableWidget.setStyleSheet("QTableWidget {background-color: rgb(255, 255, 255);}")

        
        self.pw = pg.PlotWidget(self, axisItems={'bottom': pg.DateAxisItem()})
        self.pw.setGeometry(50, 500, 1800, 250)
        self.pw.showGrid(x=True, y=True)
        self.pw.setLabel('left', 'SpO2', units='%')
        self.pw.setLabel('bottom', 'Time', units='h')
        self.pw.setTitle('SpO2')
        self.pw.enableAutoRange(axis='x', enable=True)
        self.pw.enableAutoRange(axis='y', enable=True)
        self.pw.addLegend()
        self.pw.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.pw_2 = pg.PlotWidget(self, axisItems={'bottom': pg.DateAxisItem()})
        self.pw_2.setGeometry(50, 800, 1800, 250)
        self.pw_2.showGrid(x=True, y=True)
        self.pw_2.setLabel('left', 'Signal', units='I/Q')   
        self.pw_2.setLabel('bottom', 'Time', units='h')
        self.pw_2.setTitle('Signal')
        self.pw_2.enableAutoRange(axis='x', enable=True)
        self.pw_2.enableAutoRange(axis='y', enable=True)
        self.pw_2.addLegend()
        self.pw_2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)   


    def load_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '\home', "CSV files (*.csv)")
        if fname[0]:
            df = pd.read_csv(fname[0], encoding='unicode_escape', skiprows=1, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13]).dropna()
            df['DateTime'] = pd.to_datetime(df['DateTime'])
            #set DateTime as index
            df.set_index('DateTime', inplace=True)
            df.columns = df.columns.str.replace(' ', '_')
            modes = df['O2_Mode'].unique()
            print(modes)
            print(df.columns)

            self.pw.clear()
            self.pw_2.clear()
            self.bar_plot_1.clear()
            self.bar_plot_2.clear()
            self.bar_plot_3.clear()
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)


    
        def signal_filter(df, min_signal, min_spo2):
            """Filter DataFrame by signal strength and SpO2"""
            return df[(df['Signal_I/Q'] >= min_signal) & (df['SpO2'] >= min_spo2)]

        df = signal_filter(df, 80, 40)
        
        def filter_o2_mode(df, mode):
            """Filter DataFrame by O2 mode"""
            return df[df['O2_Mode'] == mode] 

        df_m = filter_o2_mode(df, 'Manual')
        df_a = filter_o2_mode(df, 'Auto')
        print(df_m, df_a)

        def elapsed_time(dff):
            count = int(dff['O2'].count())
            return timedelta(seconds=count)

        ta = elapsed_time(df_a)
        tm = elapsed_time(df_m)
        print(ta, tm)

        def avarage_value(df, column):
            """Calculate average value of a column in a DataFrame"""
            return round(df[column].mean(), 2)            

        df_avg_a = avarage_value(df_a, 'O2')
        df_avg_m = avarage_value(df_m, 'O2')

        def rolling_average(df, column):
            """Rolling average DataFrame by O2 mode"""
            return df[column].rolling('1H').mean()

        df_m['1h_Rolling_Average'] = rolling_average(df_m, 'SpO2')
        df_a['1h_Rolling_Average'] = rolling_average(df_a, 'SpO2')
        print(df_a)
        print(df_avg_a, df_avg_m)

        def plot_data_graph_1(df, column, color, name):
            """Plot DataFrame by O2 mode"""
            return self.pw.plot(df.index, df[column], pen=color, name=name)

        def plot_data_graph_2(df, column, color, name):
            """Plot DataFrame by O2 mode"""
            return self.pw_2.plot(df.index, df[column], pen=color, name=name)

            #count unique values in O2 mode in df and plot bar graph
        def plot_bar_graph(df, column, color, name):
            """Plot DataFrame by O2 mode"""
            return self.pw_2.plot(df.index, df[column], pen=color, name=name)

        self.plot_1 = plot_data_graph_1(df_m, 'SpO2', 'r', 'Manual')
       

        def percentage(df, column):
            """Calculate percentage of unique values in a column"""
            return df[column].value_counts(normalize=True) * 100
        
        
        def graf(df, name):
            return self.pw.plot(df['SpO2'], name=name, color='r')
        graf(df_m, 'SpO2')
        
        df_p = pd.DataFrame(percentage(df, 'O2_Mode'))
        df_p.columns = ['Percentage']
        df_p.index.name = 'O2_Mode'
    
        print(df_p)
        
        xval = list(range(1,len(df_p['Percentage'])+1))
        ticks=[]
        for i, item in enumerate(df_p.index):
            ticks.append( (xval[i], item) )
        ticks = [ticks]
        print(ticks)
        
        bar_graph = pg.BarGraphItem(x=xval, height=df_p['Percentage'], width=0.5)
        #set ticks as x axis labels
        self.pw2.getAxis('bottom').setTicks(ticks)
        
        self.pw2.addItem(bar_graph)



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
