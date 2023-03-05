import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QFrame, QCheckBox, QRadioButton, QButtonGroup, QMessageBox
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
        self.setGeometry(0, 0, self.width, self.height)
        self.InitWindow()
        self.showMaximized()
        oImage = QImage("background.png")
        sImage = oImage.scaled(QtCore.QSize(self.width, self.height))  # resize Image to widgets size
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(sImage)) 
        self.setPalette(palette)
        self.df = None
        self.color_palette = {'Blue': QColor(30, 195, 225), 'Purpule': QColor(255, 88, 251), 'Yellow': QColor(255, 88, 251)}
        
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
        self.l_button.setStyleSheet("QPushButton {background-color: rgb(30, 195, 225);} \
                                    QPushButton:pressed {border: 2px solid red;}")
        self.l_button.clicked.connect(self.load_file)
        self.l_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.snap_button = QPushButton('', self)
        self.snap_button.setIcon(QIcon('snap.png'))
        self.snap_button.setIconSize(QtCore.QSize(200, 50))
        self.snap_button.move(50, 250)
        self.snap_button.resize(200, 50)
        self.snap_button.setFont(QFont('Arial', 20, QFont.Bold))
        self.snap_button.setStyleSheet("QPushButton {background-color: rgb(30, 195, 225);} \
                                        QPushButton:pressed {border: 2px solid red;}")
        self.snap_button.clicked.connect(self.take_screenshot)
        self.snap_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.bar_plot_1 = pg.PlotWidget(self)
        self.bar_plot_1.move(300, 150)
        self.bar_plot_1.resize(300, 300)
        self.bar_plot_1.setBackground('transparent')
        self.bar_plot_1.showGrid(x=True, y=True)
        self.bar_plot_1.setMouseEnabled(x=False, y=False)
        self.bar_plot_1.setMenuEnabled(False)
        self.bar_plot_1.setLogMode(x=False, y=False)
        self.bar_plot_1.setClipToView(True)
        self.bar_plot_1.setAntialiasing(True)
        self.bar_plot_1.setLimits(xMin=0, xMax=100, yMin=0, yMax=100)

        self.bar_plot_2 = pg.PlotWidget(self)
        self.bar_plot_2.move(650, 150)
        self.bar_plot_2.resize(300, 300)
        self.bar_plot_2.setBackground('transparent')
        self.bar_plot_2.showGrid(x=True, y=True)
        self.bar_plot_2.setMouseEnabled(x=False, y=False)
        self.bar_plot_2.setMenuEnabled(False)
        self.bar_plot_2.setLogMode(x=False, y=False)
        self.bar_plot_2.setClipToView(True)
        self.bar_plot_2.setAntialiasing(True)
        self.bar_plot_2.setLimits(xMin=0, xMax=100, yMin=0, yMax=100)

        self.table = QtWidgets.QTableWidget(self)
        self.table.move(1000, 150)
        self.table.resize(500, 300)
        self.table.setRowCount(9)
        self.table.setColumnCount(2)

        self.table.setStyleSheet(
    "background-color: transparent; color: rgb(30, 195, 225); border: 1px solid black;"
)

        self.table.setHorizontalHeaderLabels(['Parameter', 'Value'])
        font = QtGui.QFont()
        font.setPointSize(16)   
        self.table.setFont(font)
        self.table.horizontalHeader().setStyleSheet(
    "background-color: rgb(30, 195, 225); color: rgb(40, 81, 128); font-size: 20pt;"
)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setStyleSheet("background-color: transparent; border: none;")
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)


        self.label_2 = QLabel(self)
        self.label_2.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.label_2.setLineWidth(2)
        self.label_2.resize(200, 100)
        self.label_2.move(1600, 150)

        self.label_3 = QLabel(self)
        self.label_3.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.label_3.setLineWidth(2)
        self.label_3.resize(200, 100)
        self.label_3.move(1600, 350)
      
        self.radio_button_1 = QRadioButton('SpO2', self)
        self.radio_button_1.move(50, 450)
        self.radio_button_1.resize(200, 50)
        self.radio_button_1.setFont(QFont('Arial', 20, QFont.Bold))
        self.radio_button_1.setStyleSheet("background-color: transparent; color: rgb(30, 195, 225);")
        self.radio_button_1.clicked.connect(self.radiobutton1)
        self.radio_button_1.setChecked(True)
        self.radio_button_1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.radio_button_2 = QRadioButton('Pulse Rate', self)
        self.radio_button_2.move(150, 450)
        self.radio_button_2.resize(200, 50)
        self.radio_button_2.setFont(QFont('Arial', 20, QFont.Bold))
        self.radio_button_2.setStyleSheet("background-color: transparent; color: rgb(30, 195, 225);")
        self.radio_button_2.clicked.connect(self.radiobutton1)
        self.radio_button_2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.radio_button_3 = QRadioButton('Perfusion index', self) 
        self.radio_button_3.move(300, 450)
        self.radio_button_3.resize(200, 50)
        self.radio_button_3.setFont(QFont('Arial', 20, QFont.Bold))
        self.radio_button_3.setStyleSheet("background-color: transparent; color: rgb(30, 195, 225);")
        self.radio_button_3.clicked.connect(self.radiobutton1)
        self.radio_button_3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.buttongroup1 = QButtonGroup()
        self.buttongroup1.addButton(self.radio_button_1)
        self.buttongroup1.addButton(self.radio_button_2)
        self.buttongroup1.addButton(self.radio_button_3)

        self.pw = pg.PlotWidget(self, axisItems={'bottom': pg.DateAxisItem()})
        self.pw.setGeometry(50, 500, 1800, 250)
        self.pw.showGrid(x=True, y=True)
        self.pw.setLabel('bottom', 'Time', units='h')
        self.pw.enableAutoRange(axis='x', enable=True)
        self.pw.enableAutoRange(axis='y', enable=True)
        self.pw.setBackground('transparent')
        self.pw.addLegend()
        self.pw.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.radio_button_4 = QRadioButton('Flow', self)
        self.radio_button_4.move(50, 750)
        self.radio_button_4.resize(200, 50)    
        self.radio_button_4.setFont(QFont('Arial', 20, QFont.Bold))
        self.radio_button_4.setStyleSheet("background-color: transparent; color: rgb(30, 195, 225);")
        self.radio_button_4.toggled.connect(self.radiobutton2)
        self.radio_button_4.setChecked(True)
        self.radio_button_4.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.radio_button_5 = QRadioButton('FiO2', self)
        self.radio_button_5.move(150, 750)
        self.radio_button_5.resize(200, 50)    
        self.radio_button_5.setFont(QFont('Arial', 20, QFont.Bold))
        self.radio_button_5.setStyleSheet("background-color: transparent; color: rgb(30, 195, 225);")
        self.radio_button_5.toggled.connect(self.radiobutton2)
        self.radio_button_5.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        
        self.buttongroup2 = QButtonGroup()
        self.buttongroup2.addButton(self.radio_button_4)
        self.buttongroup2.addButton(self.radio_button_5)
        
        self.pw2 = pg.PlotWidget(self, axisItems={'bottom': pg.DateAxisItem()})
        self.pw2.setGeometry(50, 800, 1800, 250)
        self.pw2.showGrid(x=True, y=True)
        self.pw2.setLabel('bottom', 'Time', units='h')
        self.pw2.enableAutoRange(axis='x', enable=True)
        self.pw2.enableAutoRange(axis='y', enable=True)
        self.pw2.setBackground('transparent')
        self.pw2.addLegend()
        self.pw2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        

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

        
        df_p = pd.DataFrame(DataProcessor(df).percentage('O2_Mode'))
        df_p.columns = ['Percentage']
        df_p.index.name = 'O2_Mode'
        
        xval = list(range(1,len(df_p['Percentage'])+1))
        ticks=[]
        for i, item in enumerate(df_p.index):
            ticks.append( (xval[i], item) )
        ticks = [ticks]

        bar_plot = pg.BarGraphItem(x=xval, height=df_p['Percentage'], width=0.5)
        bar_plot.setOpts(brush=QColor(255, 88, 251))    
        self.bar_plot_1.getAxis('bottom').setTicks(ticks)
        self.bar_plot_1.addItem(bar_plot)

        df_filter_2 = DataProcessor(df).signal_filter_v(80, 90)
        self.df_filter_auto = DataProcessor(df_filter_2).filter_o2_mode_v('Auto')
        df_percentage = DataProcessor(self.df_filter_auto).percentage('O2')
        df_o2_dis = DataProcessor(self.df_filter_auto).o2_distribution()
        table_val = DataProcessor(self.df_filter_auto).calculate_table()
        roll_o2 = DataProcessor(self.df_filter_auto).rolling_mean('O2', '6H', self.df_filter_auto['O2'].mean())
        self.roll_spo2 = DataProcessor(self.df_filter_auto).rolling_mean('SpO2', '6H', self.df_filter_auto['SpO2'].mean())
        self.roll_pulse_rate = DataProcessor(self.df_filter_auto).rolling_mean('PR', '6H', self.df_filter_auto['PR'].mean())
        self.roll_PI = DataProcessor(self.df_filter_auto).rolling_mean('PI', '6H', self.df_filter_auto['PI'].mean())
        self.roll_FiO2 = DataProcessor(self.df_filter_auto).rolling_mean('O2', '6H', self.df_filter_auto['O2'].mean())

        bar_plot_2 = pg.BarGraphItem(x=df_o2_dis.index, height=df_o2_dis['Percentage'], width=0.5)
        bar_plot_2.setOpts(brush=QColor(255, 176 ,88))
        self.bar_plot_2.addItem(bar_plot_2)

# Loop to fill the table from the dataframe in OAMDataMan
        for i, row in table_val.iterrows():
            param_item = QTableWidgetItem(row['Parameter'])
            value_item = QTableWidgetItem(str(row['Value']))
            self.table.setItem(i, 0, param_item)
            self.table.setItem(i, 1, value_item)

        self.label_2.setText(f"<p style='font-size:14pt'>Avarege FiO2 in Auto mode</p><p style='font-size:16pt'>{table_val.loc[1, 'Value']}%</p>")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("background-color: transparent; color: rgb(30, 195, 225);")

        self.label_3.setText(f"<p style='font-size:14pt'>Time in Auto Mode</p><p style='font-size:16pt'>{DataProcessor(df).elapsed_time()}</p>")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setStyleSheet("background-color: transparent; color: rgb(30, 195, 225);")

        self.pw.clear()
        self.pw.plot(self.roll_spo2, pen=pg.mkPen(color=(255, 88, 251), width=3), name='O2')
        self.pw.plot(self.df_filter_auto['SpO2_Target'], pen=pg.mkPen(color='r', width=1), name='SpO2_Target')
        self.pw.setLabel('left', 'SpO2', units='%')

        self.pw2.clear()
        self.pw2.plot(self.df_filter_auto['Flow_(L/min)'], pen=pg.mkPen(color=self.color_palette['Yellow'], width=3), name='SpO2')
        self.pw2.setLabel('left', 'Flow', units='L/min')

    def radiobutton1(self):
        if self.radio_button_1.isChecked():
            self.pw.clear()
            self.pw.plot(self.roll_spo2, pen=pg.mkPen(color=self.color_palette['Blue'], width=3), name='SpO2')
            self.pw.setLabel('left', 'SpO2', units='%')
            self.pw.plot(self.df_filter_auto['SpO2_Target'], pen=pg.mkPen(color='r', width=2), name='SpO2_Target')
        if self.radio_button_2.isChecked():    
            self.pw.clear()
            self.pw.plot(self.roll_pulse_rate, pen=pg.mkPen(color=(255, 176, 88), width=3), name='Pulse Rate')
            self.pw.setLabel('left', 'Pulse Rate', units='bpm')
        if self.radio_button_3.isChecked():
            self.pw.clear()
            self.pw.plot(self.roll_PI, pen=pg.mkPen(color=(30, 195, 225), width=3), name='PI')
            self.pw.setLabel('left', 'PI', units='')
    def radiobutton2(self):
        if self.radio_button_4.isChecked():
            self.pw2.clear()
            self.pw2.plot(self.df_filter_auto['Flow_(L/min)'], pen=pg.mkPen(color=self.color_palette['Yellow'], width=3), name='SpO2')
            self.pw2.setLabel('left', 'Flow', units='L/min')
        if self.radio_button_5.isChecked():
            self.pw2.clear()
            self.pw2.plot(self.roll_FiO2, pen=pg.mkPen(color=self.color_palette['Yellow'], width=3), name='FiO2')
            self.pw2.setLabel('left', 'FiO2', units='%')

    def take_screenshot(self):
        """Take a screenshot of the current window and save it to a file"""
        screen = QtGui.QGuiApplication.primaryScreen()
        pixmap = screen.grabWindow(0)
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Screenshot", "", "PNG Files (*.png)", options=options
        )
        if file_name:
            pixmap.save(file_name, "PNG")
        
    
app = QApplication(sys.argv)
if __name__ == '__main__':
    window = MainWindow()
    sys.exit(app.exec_())