import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        button1 = QPushButton('Button 1')
        button2 = QPushButton('Button 2')
        button3 = QPushButton('Button 3')
        button4 = QPushButton('Button 4')
        button5 = QPushButton('Button 5')
        button6 = QPushButton('Button 6')
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(button1)
        hbox1.addWidget(button2)
        hbox1.addWidget(button3)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(button4)
        hbox2.addWidget(button5)
        hbox2.addWidget(button6)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        
        self.setLayout(vbox)
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Two Rows of Three Buttons')
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
