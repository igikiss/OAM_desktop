import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont, QPixmap, QCursor
import pandas as pd
import numpy as np
from datetime import timedelta
import pyqtgraph as pg
import polars as pl



class MainWindow(QMainWindow):
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

   
        self.pw2 = pg.PlotWidget(self, background='w')
        self.pw2.setGeometry(50, 800, 1800, 250)
        self.pw2.showGrid(x=True, y=True)
        self.pw2.setLabel('left', 'O2', units='%')
        self.pw2.setLabel('bottom', 'Time', units='h')
        self.pw2.setTitle('O2')
        self.pw2.enableAutoRange(axis='x', enable=True)
        self.pw2.enableAutoRange(axis='y', enable=True)
        self.pw2.addLegend()
        self.pw2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        



       
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

        def signal_filter(df, min_signal, min_spo2):
            """Filter DataFrame by signal strength and SpO2"""
            return df[(df['Signal_I/Q'] >= min_signal) & (df['SpO2'] >= min_spo2)]

        df_f = signal_filter(df, 80, 40)
        df_f.info()

   
        def filter_o2_mode(df, mode):
            """Filter DataFrame by O2 mode"""
            return df[df['O2_Mode'] == mode] 

        df_m = filter_o2_mode(df, 'Manual')
        df_a = filter_o2_mode(df, 'Auto')

   #calculate from df percetge of O2_Mode unque values
        def percentage(df, column):
            """Calculate percentage of unique values in a column"""
            return df[column].value_counts(normalize=True) * 100

        df_p = pd.DataFrame(percentage(df, 'O2_Mode'))

#create a dataframe with the percentage of each O2_Mode
        df_p = pd.DataFrame(percentage(df, 'O2_Mode'))
        df_p.columns = ['Percentage']
        df_p.index.name = 'O2_Mode'
        df_p.reset_index(inplace=True)
        print(df_p)
       

        def graf(df, name):
            return self.pw.plot(df['SpO2'], name=name, color='r')
        graf(df_m, 'SpO2')

        bar_graph = pg.BarGraphItem(x=np.arange(len(df_p.columns)), height=df_p['Percentage'], width=0.6, brush='b')
        # make each bar of the bar graph nema of the df_p index
        bar_graph.setOpts(names=df_p['O2_Mode'])




      # Set the x-axis labels to be the column names of df_p
        self.pw2.setOpts(x0=np.arange(len(df_p.columns))-0.3, x1=np.arange(len(df_p.columns))+0.3, labels=df.columns)
        self.pw2.addItem(bar_graph)


  
        #self.pw.plot(df_m['SpO2'], pen='r', name='Manual')
    
       
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


