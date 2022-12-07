# Import the necessary modules from PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

# Create a widget with a button
class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a button
        self.button = QPushButton('Click me')

        # Add the button to the layout of the widget
        layout = QHBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

        # Set the size and position of the button relative to the window
        self.button.setGeometry(0, 0, self.width(), self.height() / 2)

# Create an application and show the main widget
app = QApplication([])
main_widget = MainWidget()
main_widget.show()
app.exec_()


