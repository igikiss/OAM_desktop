import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QComboBox, QWidget

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(["Graph 1", "Graph 2", "Graph 3"])
        self.combo_box.currentIndexChanged.connect(self.print_graph)

    def print_graph(self, index):
        graph_data = self.get_graph_data(index)
        plt.plot(graph_data)
        plt.show()

    def get_graph_data(self, index):
        if index == 0:
            return [1, 2, 3, 4]
        elif index == 1:
            return [5, 6, 7, 8]
        else:
            return [9, 10, 11, 12]

app = QApplication([])
widget = MyWidget()
widget.show()
app.exec_()
