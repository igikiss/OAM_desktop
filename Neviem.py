import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # create a vertical layout
        vbox = QVBoxLayout()

        # create a horizontal layout and add widgets to it
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('Name:'))
        hbox.addWidget(QLineEdit())

        # add the horizontal layout to the vertical layout
        vbox.addLayout(hbox)

        # create a grid layout
        grid = QGridLayout()

        # add labels and line edits to the grid layout
        grid.addWidget(QLabel('Age:'), 0, 0)
        grid.addWidget(QLineEdit(), 0, 1)
        grid.addWidget(QLabel('Address:'), 1, 0)
        grid.addWidget(QLineEdit(), 1, 1)

        # add the grid layout to the vertical layout
        vbox.addLayout(grid)

        # add a button to the vertical layout
        vbox.addWidget(QPushButton('Submit'))

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Example')
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
