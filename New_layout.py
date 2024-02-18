import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QFrame, QFileDialog, QMessageBox
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
            """This function creates a button with the given name and returns it.
            We use these buttons  tp "Load Data" and "Snap Shot" in the GUI."""
            button = QPushButton(name)
            button.setFixedSize(200, 30)
            button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            button.setStyleSheet("border-radius: 10px; background-color: rgb(30, 195, 225); color: white;")
            return button
        
        def bar_graph_func():
            """B ar_graph_func creates a bar graph and returns it. We use this to display the bar graph in the GUI.
            We use these bar graphs to display the data of percetual use of FiO2 and Peercentual mode the device was used."""
            bar_graph = pg.PlotWidget()
            bar_graph.resize(300, 100)
            bar_graph.setBackground('transparent')
            bar_graph.showGrid(x=True, y=True)
            bar_graph.resize(300, 100)
            return bar_graph
        
        def label_window(name):
            """Label_window create labels whoch display the mean value of FiO2 and sesiion time"""
            label = QLabel(name)
            label.setFrameStyle(QFrame.Box | QFrame.Plain)
            label.setLineWidth(1)
            return label
        
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
        button1.clicked.connect(self.load_file)
        
        button2 = button_func('Snap Shot')
        button2.setIcon(QIcon('snap.png'))
        button2.setIconSize(QtCore.QSize(30, 30))
        button2.clicked.connect(self.take_screenshot)
        
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
        
        label_window1 = label_window('Patient Information')
        label_window2 = label_window('Ventilator Information')
        
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
        
        layout4 = QVBoxLayout()
        layout4.addWidget(label_window1)
        layout4.addWidget(label_window2)
    
        layout3.addLayout(layout4)
        
        layout5 = QHBoxLayout()
        layout5.addWidget(radio1)
        layout5.addWidget(radio2)
        layout5.addWidget(radio3)
        
        layout6 = QHBoxLayout()
        layout6.addWidget(plot1)
        
        layout7 = QHBoxLayout()
        layout7.addWidget(radio4)
        layout7.addWidget(radio5)
        layout7.addWidget(radio6)
        
        layout8 = QHBoxLayout() 
        layout8.addWidget(plot2)
        
        layout.addLayout(layout2) 
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(layout6)
        layout.addLayout(layout7)
        layout.addLayout(layout8)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.show()
        
    def load_file(self):
        """Load a CSV file into a dataframe"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                df = pd.read_csv(file_path, encoding='unicode_escape', skiprows=1, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]).dropna()
                df['DateTime'] = pd.to_datetime(df['DateTime'])
                df.set_index('DateTime', inplace=True)
                df.columns = df.columns.str.replace(' ', '_')
                self.df = df
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error loading CSV:\n{str(e)}")
                
    def take_screenshot(self):
        """Take a screenshot of the current window and save it to a file"""
        screen = QtGui.QGuiApplication.primaryScreen()
        pixmap = screen.grabWindow(0)
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "OAM Screenshot", "", "PNG Files (*.png)", options=options
        )
        if file_name:
            pixmap.save(file_name, "PNG")
            
    
        
            
            
app = QApplication(sys.argv)
if __name__ == '__main__':
    window = MainWindow()
    sys.exit(app.exec_())