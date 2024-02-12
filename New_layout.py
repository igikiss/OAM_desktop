import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont, QPixmap, QCursor, QImage, QColor
import pyqtgraph as pg
import pandas as pd
from Process import DataProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "OAM Desktop"
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.width = self.screen.width()
        self.height = self.screen.height()
        self.top = 0
        self.left = 0
        self.setGeometry(100, 100, 640, 480)
        self.InitWindow()
        self.showMaximized()
        oImage = QImage("background.png")
        sImage = oImage.scaled(QtCore.QSize(self.width, self.height))  # resize Image to widgets size
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(sImage)) 
        self.setPalette(palette)
        self.df = None
        self.color_palette = {'Blue': QColor(30, 195, 225), 'Purpule': QColor(255, 88, 251), 'Yellow': QColor(255, 176 ,88)}

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
  
        self.label_1 = QLabel('VAPOTHERM OAM VIEWER')
        self.label_1.setFont(QFont('Arial', 30, QFont.Bold))
        self.label_1.setStyleSheet("color: rgb(30, 195, 225);")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label_1)
        layout.addStretch(1) 

        def button_func(name):
            button = QPushButton(name)
            button.setFixedSize(200, 30)
            # make button round 
            button.setStyleSheet("border-radius: 10px; background-color: rgb(30, 195, 225); color: white;")
            return button
        
        def bar_graph_func():
            bar_graph = pg.PlotWidget()
            bar_graph.resize(300, 100)
            bar_graph.setBackground('transparent')
            bar_graph.showGrid(x=True, y=True)
            bar_graph.resize(300, 100)
            return bar_graph
        
        def radio_button_func(name):
            radio = QtWidgets.QRadioButton(name)
            return radio
        
        def plot_func():
            plot = pg.PlotWidget()
            plot.setBackground('transparent')
            plot.showGrid(x=True, y=True)
            plot.setLabel('bottom', 'Time', units='h')
            plot.enableAutoRange(axis='x', enable=True)
            plot.enableAutoRange(axis='y', enable=True)
            plot.addLegend()
            return plot
        
        button1 = button_func('Load Data')
        button2 = button_func('Snap Shot')
        button2.setIcon(QIcon('snap.png'))
        button2.setIconSize(QtCore.QSize(30, 30))
        
        bar_graph = bar_graph_func()
        bar_graph2 = bar_graph_func()
        
        table1 = pg.TableWidget()
        table1.resize(300, 100)
        table1.setStyleSheet(
            "background-color: transparent; color: rgb(30, 195, 225); border: 1px solid black;"
        )
        table1.setRowCount(9)
        table1.setColumnCount(2)
        table1.setHorizontalHeaderLabels(['Parameter', 'Value'])
        font = QFont()
        font.setPointSize(12)
        table1.horizontalHeader().setFont(font)
        table1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table1.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table1.verticalHeader().setFont(font)
        
        radio1 = radio_button_func('Option 1')
        radio2 = radio_button_func('Option 2')
        radio3 = radio_button_func('Option 3')
        
        plot1 = plot_func()
        
        radio4 = radio_button_func('Option 4')
        radio5 = radio_button_func('Option 5')
        radio6 = radio_button_func('Option 6')
        
        plot2 = plot_func()

        layout2 = QHBoxLayout()
        layout2.addWidget(button1)
        layout2.addWidget(button2)
        
        layout3 = QHBoxLayout()
        layout3.addWidget(bar_graph)
        layout3.addWidget(bar_graph2)
        layout3.addWidget(table1)
        
        layout4 = QHBoxLayout()
        layout4.addWidget(radio1)
        layout4.addWidget(radio2)
        layout4.addWidget(radio3)
        
        layout5 = QHBoxLayout()
        layout5.addWidget(plot1)
        
        layout6 = QHBoxLayout()
        layout6.addWidget(radio4)
        layout6.addWidget(radio5)
        layout6.addWidget(radio6)
        
        layout7 = QHBoxLayout() 
        layout7.addWidget(plot2)
        
        layout.addLayout(layout2)  # Add the QHBoxLayout to the QVBoxLayout
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(layout6)
        layout.addLayout(layout7)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.show()
        
app = QApplication(sys.argv)
if __name__ == '__main__':
    window = MainWindow()
    sys.exit(app.exec_())