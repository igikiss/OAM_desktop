from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QMainWindow, QAction, qApp, QTextEdit, QLabel, QGridLayout, QWidget, QFileDialog, QFrame, QComboBox, QTableWidget, QTableWidgetItem
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

        self.title = "OAM Desktop"
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.width = self.screen.width()
        self.height = self.screen.height()
        self.top = self.screen.height()
        self.left = self.screen.width()
        self.setGeometry(0, 0, self.width, self.height)
        self.InitWindow()
        self.showMaximized()

    def InitWindow(self):
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        
        self.label = QLabel(self)
        self.label_1 = QLabel('VAPOTHERM OAM VIEWER', self)
        self.label_1.setFont(QFont('Arial', 40, QFont.Bold))
        self.label_1.resize(600, 50)
        self.label_1.setStyleSheet("color: rgb(30, 195, 225);")
        self.label_1.move(700, 50)

        
        self.l_button = QPushButton('Load File', self)
        self.l_button.move(50, 100)
        self.l_button.resize(200, 50)
        self.l_button.setFont(QFont('Arial', 20, QFont.Bold))
        self.l_button.setStyleSheet("background-color: rgb(30, 195, 225);")
        self.l_button.clicked.connect(self.load_file)
        self.l_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.p_button = QPushButton('PDF', self)
        self.p_button.move(50, 100)
        self.p_button.resize(200, 50)
        self.p_button.setFont(QFont('Arial', 20, QFont.Bold))
        self.p_button.setStyleSheet("background-color: rgb(30, 195, 225);")
        #self.p_button.clicked.connect(self.pdf)
        self.p_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))


        self.roll_box = QComboBox(self)
        self.roll_box.move(50, 500)
        self.roll_box.resize(200, 50)
        self.roll_box.setFont(QFont('Arial', 20, QFont.Bold))
        self.roll_box.setStyleSheet("background-color: rgb(30, 195, 225);")
        self.roll_box.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.roll_box.addItem("Graph_1")
        self.roll_box.addItem("Graph_2")
        
       
        #self.label_2 = QLabel(self)
        #self.label_2.setFrameStyle(QFrame.Box | QFrame.Plain)
        #self.label_2.setLineWidth(2)
        #self.label_2.resize(200, 100)
        #self.label_2.move(50, 50)
        #self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);")

        #self.label_3 = QLabel(self)
        #self.label_3.setFrameStyle(QFrame.Box | QFrame.Plain)
        #self.label_3.setLineWidth(2)
        #self.label_3.resize(200, 100)
        #self.label_3.move(300, 50)
        #self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);")

        # add table
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(50, 150, 200, 300)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Parameter', 'Value'])
        self.tableWidget.setVerticalHeaderLabels(['SpO2', 'Pulse Rate', 'Signal'])
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tableWidget.setFont(QFont('Arial', 20, QFont.Bold))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.tableWidget.setLineWidth(2)
        self.tableWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tableWidget.item(0, 0).setBackground(QtGui.QColor(30, 195, 225))
        self.tableWidget.item(1, 0).setBackground(QtGui.QColor(30, 195, 225))
        self.tableWidget.item(2, 0).setBackground(QtGui.QColor(30, 195, 225))
        self.tableWidget.item(0, 1).setBackground(QtGui.QColor(255, 255, 255))
        self.tableWidget.item(1, 1).setBackground(QtGui.QColor(255, 255, 255))
        self.tableWidget.item(2, 1).setBackground(QtGui.QColor(255, 255, 255))
        self.tableWidget.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.item(1, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.item(2, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.item(0, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.item(1, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.item(2, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.item(0, 0).setForeground(QtGui.QColor(255, 255, 255))
        self.tableWidget.item(1, 0).setForeground(QtGui.QColor(255, 255, 255))
        self.tableWidget.item(2, 0).setForeground(QtGui.QColor(255, 255, 255))
        self.tableWidget.item(0, 1).setForeground(QtGui.QColor(0, 0, 0))
        self.tableWidget.item(1, 1).setForeground(QtGui.QColor(0, 0, 0))



        self.pw = pg.PlotWidget(self, axisItems={'bottom': pg.DateAxisItem()})
        self.pw.setGeometry(50, 600, 1800, 250)
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
      

  
        #self.label_2.setText(f"<p style='font-size:12pt'>Avarege FiO2 in Auto mode</p><p style='font-size:16pt'>{avarage_value(df_a, 'O2')}</p>")
        #self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        #self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);")

        #self.label_3.setText(f"<p style='font-size:12pt'>Time in Auto Mode</p><p style='font-size:16pt'>{elapsed_time(df_a)}</p>")
        #self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        #self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);")

            
        #self.pw.plot(df_a.index, df_a['SpO2'], pen='#21221f', mame='SpO2')
        #create a plot for each mode and add to plot widget x axis is DateTime, y axis is SpO2
        #self.pw.plot(df_a['SpO2'], pen='r', name='Auto')
        #highlight the SpO2 values that are below 90 with different color and above 90 with different color

        self.pw.plot(df_a['SpO2'], pen='r', name='SpO2')
        
        #plot second y axis in the same plot widget

        self.pw.plot(df_a['1h_Rolling_Average'], pen='g', name='1h_Rolling_Average')
        #self.pw.plot(df_m['SpO2'], pen='b', name='Manual')
        self.pw_2.plot(df_a['PI'], pen='b', name='/erfusiion index')
    
    #add data to pie chart
        self.pie_chart.add_data([df_avg_a, df_avg_m], ['Auto', 'Manual'])
        self.pie_chart.update()


        
            


def main():
    app = QtWidgets.QApplication(sys.argv)
    main =MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()




