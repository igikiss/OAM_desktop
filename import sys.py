import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        label = QLabel("Hello, World!", self)
        label.move(50, 50)
        self.setCentralWidget(label)

        self.setWindowTitle("MainWindow")
        self.show()


app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
