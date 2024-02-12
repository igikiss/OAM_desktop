import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QFrame, QCheckBox, QRadioButton, QButtonGroup, QMessageBox, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont, QPixmap, QCursor, QImage, QColor
import pyqtgraph as pg 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Window")
        self.setGeometry(100, 100, 640, 480)
        self.initUI()

    def initUI(self):
        # Create label and add to top layout
        label_hello = QLabel("Vapotherm OAM", self)
        label_hello.setStyleSheet("font-size: 24px; font-weight: bold;")
        label_hello.resize(100, 50)
        label_hello.setAlignment(QtCore.Qt.AlignCenter)

        # Create layouts for three rows of widgets
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Button 1"))
        layout1.addWidget(QLabel("Button 2"))
        layout1.addWidget(QLabel("Button 3"))
        layout1.addWidget(QLabel("Button 4"))

        button5 = QPushButton("Button 5")
        button5.setFixedSize(100, 50)
        button6 = QPushButton("Button 6")
        button6.setFixedSize(120, 60)
        button7 = QPushButton("Button 7")
        button7.setFixedSize(140, 70)
        button8 = QPushButton("Button 8")
        button8.setFixedSize(160, 80)

        layout2 = QHBoxLayout()
        layout2.addWidget(button5)
        layout2.addWidget(button6)
        layout2.addWidget(button7)
        layout2.addWidget(button8)

        button9 = QPushButton("Button 9")
        button9.setFixedSize(180, 90)
        button10 = QPushButton("Button 10")
        button10.setFixedSize(200, 100)
        button11 = QPushButton("Button 11")
        button11.setFixedSize(220, 110)
        button12 = QPushButton("Button 12")
        button12.setFixedSize(240, 120)

        layout3 = QHBoxLayout()
        layout3.addWidget(button9)
        layout3.addWidget(button10)
        layout3.addWidget(button11)
        layout3.addWidget(button12)

        # Create grid layout and add three row layouts to it
        grid_layout = QGridLayout()
        grid_layout.addLayout(layout1, 0, 0)
        grid_layout.addLayout(layout2, 1, 0)
        grid_layout.addLayout(layout3, 2, 0)

        # Create top layout and add label to it
        top_layout = QVBoxLayout()
        top_layout.addWidget(label_hello, alignment=QtCore.Qt.AlignCenter)

        # Create main layout and add top and grid layouts to it
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(grid_layout)

        # Set main layout
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.show()

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())